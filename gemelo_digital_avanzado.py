#!/usr/bin/env python3
"""
GEMELO DIGITAL AVANZADO - Škoda Octavia 1.5 TSI 2024
Con: Filtro Kalman, validación datos, agregación temporal, diagnóstico automático
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import signal
from scipy.fft import fft, fftfreq
from scipy.ndimage import uniform_filter1d
import json
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# ==================== FILTRO KALMAN ====================

class FiltroKalman:
    """Filtro Kalman 1D para suavizar datos ruidosos"""
    
    def __init__(self, proceso_ruido=0.001, medicion_ruido=0.1, valor_inicial=0):
        """
        Args:
            proceso_ruido: Varianza del proceso (qué tanto cambia cada paso)
            medicion_ruido: Varianza de medición (cuán ruidoso es el sensor)
            valor_inicial: Estimación inicial
        """
        self.q = proceso_ruido  # Ruido del proceso
        self.r = medicion_ruido  # Ruido de medición
        self.x = valor_inicial   # Estimación
        self.p = 1.0            # Error de estimación
        self.k = 0.0            # Ganancia Kalman
    
    def actualizar(self, medicion):
        """Actualizar con nueva medición y retornar estimación suavizada"""
        # Predicción
        self.p = self.p + self.q
        
        # Ganancia de Kalman
        self.k = self.p / (self.p + self.r)
        
        # Actualización
        self.x = self.x + self.k * (medicion - self.x)
        self.p = (1 - self.k) * self.p
        
        return self.x
    
    def procesar_serie(self, datos):
        """Procesar una serie completa de datos"""
        resultado = []
        for valor in datos:
            if pd.notna(valor):
                resultado.append(self.actualizar(valor))
            else:
                resultado.append(np.nan)
        return np.array(resultado)


class ValidadorDatos:
    """Validación y limpieza de datos OBD2"""
    
    # Rangos válidos para Škoda Octavia 1.5 TSI 2024
    RANGOS_VALIDOS = {
        'rpm': (0, 7000),
        'speed': (0, 250),
        'consumoInstantaneo': (0, 20),
        'power': (0, 120),
        'coolantTemp': (0, 130),
        'oilTemp': (0, 130),
        'oilPressure': (0, 10),
        'coolantLevel': (0, 100),
        'oilLevel': (0, 100),
        'fuelLevel': (0, 100),
        'fuelPressure': (0, 10),
        'boostPressure': (0, 2),
        'tirePressureLF': (1.5, 2.8),
        'tirePressureRF': (1.5, 2.8),
        'tirePressureLR': (1.5, 2.8),
        'tirePressureRR': (1.5, 2.8),
        'vibracionMagnitud': (0, 2),
        'acelerometerX': (-5, 5),
        'acelerometerY': (-5, 5),
        'acelerometerZ': (-5, 5),
        'dsgFluidTemp': (0, 150),
    }
    
    @staticmethod
    def validar_valor(columna, valor):
        """Validar un valor individual"""
        if pd.isna(valor):
            return True  # NaN es válido (se interpola)
        
        if columna in ValidadorDatos.RANGOS_VALIDOS:
            min_val, max_val = ValidadorDatos.RANGOS_VALIDOS[columna]
            return min_val <= valor <= max_val
        
        return True
    
    @staticmethod
    def limpiar_datos(df):
        """Limpiar y validar DataFrame completo"""
        df_limpio = df.copy()
        estadisticas = {
            'registros_iniciales': len(df),
            'outliers_eliminados': 0,
            'interpolaciones': 0,
        }
        
        # 1. Detectar y marcar outliers con IQR
        for columna in df_limpio.select_dtypes(include=[np.number]).columns:
            if columna in ValidadorDatos.RANGOS_VALIDOS:
                Q1 = df_limpio[columna].quantile(0.25)
                Q3 = df_limpio[columna].quantile(0.75)
                IQR = Q3 - Q1
                
                limite_inferior = Q1 - 1.5 * IQR
                limite_superior = Q3 + 1.5 * IQR
                
                outliers = ((df_limpio[columna] < limite_inferior) | 
                           (df_limpio[columna] > limite_superior))
                
                df_limpio.loc[outliers, columna] = np.nan
                estadisticas['outliers_eliminados'] += outliers.sum()
        
        # 2. Validar rangos
        for columna in ValidadorDatos.RANGOS_VALIDOS:
            if columna in df_limpio.columns:
                min_val, max_val = ValidadorDatos.RANGOS_VALIDOS[columna]
                mascara = ((df_limpio[columna] < min_val) | 
                          (df_limpio[columna] > max_val))
                df_limpio.loc[mascara, columna] = np.nan
        
        # 3. Interpolar valores faltantes
        df_limpio = df_limpio.interpolate(method='linear', limit_direction='both')
        estadisticas['interpolaciones'] = df_limpio.isna().sum().sum()
        
        # 4. Forward/backward fill para NaNs restantes
        df_limpio = df_limpio.fillna(method='ffill').fillna(method='bfill')
        
        estadisticas['registros_finales'] = len(df_limpio)
        estadisticas['porcentaje_valido'] = (estadisticas['registros_finales'] / 
                                            estadisticas['registros_iniciales'] * 100)
        
        return df_limpio, estadisticas
    
    @staticmethod
    def aplicar_filtro_kalman(df, columnas_filtrar=None):
        """Aplicar filtro Kalman a columnas especificadas"""
        df_filtrado = df.copy()
        
        if columnas_filtrar is None:
            columnas_filtrar = ['rpm', 'speed', 'consumoInstantaneo', 'power', 
                              'vibracionMagnitud']
        
        for columna in columnas_filtrar:
            if columna in df_filtrado.columns:
                # Configurar filtro según la columna
                if columna == 'rpm':
                    filtro = FiltroKalman(proceso_ruido=10, medicion_ruido=50)
                elif columna == 'vibracionMagnitud':
                    filtro = FiltroKalman(proceso_ruido=0.0001, medicion_ruido=0.01)
                else:
                    filtro = FiltroKalman(proceso_ruido=0.01, medicion_ruido=0.1)
                
                df_filtrado[columna] = filtro.procesar_serie(df_filtrado[columna].values)
        
        return df_filtrado


class AgregadorTemporal:
    """Agregación temporal de datos para reducir volumen"""
    
    @staticmethod
    def agregar_por_intervalo(df, intervalo_segundos=5):
        """
        Agregar datos por intervalo temporal
        
        Args:
            df: DataFrame con columna 'timestamp'
            intervalo_segundos: Intervalo de agregación
        """
        # Asumir que hay un registro cada 100ms
        registros_por_intervalo = int(intervalo_segundos / 0.1)
        
        df_agregado = df.copy()
        
        # Columnas numéricas
        cols_numericas = df_agregado.select_dtypes(include=[np.number]).columns
        
        # Aggregación por grupos
        agg_dict = {}
        for col in cols_numericas:
            if col in ['rpm', 'power', 'speed', 'consumoInstantaneo']:
                agg_dict[col] = 'mean'  # Media para continuos
            elif col in ['tirePressureLF', 'tirePressureRF', 'tirePressureLR', 'tirePressureRR']:
                agg_dict[col] = 'mean'  # Media para presiones
            elif col == 'vibracionMagnitud':
                agg_dict[col] = 'max'  # Máximo para vibraciones (conservador)
            else:
                agg_dict[col] = 'last'  # Último valor
        
        df_agregado['grupo'] = np.arange(len(df_agregado)) // registros_por_intervalo
        df_agregado = df_agregado.groupby('grupo').agg(agg_dict)
        df_agregado = df_agregado.drop('grupo', axis=1, errors='ignore')
        
        return df_agregado
    
    @staticmethod
    def remuestrear(df, frecuencia='5S'):
        """Remuestrear a frecuencia específica (más robusto)"""
        if 'timestamp' in df.columns:
            df = df.set_index('timestamp')
        
        cols_numericas = df.select_dtypes(include=[np.number]).columns
        
        agg_dict = {}
        for col in cols_numericas:
            if col in ['vibracionMagnitud']:
                agg_dict[col] = 'max'
            elif col in ['fuelLevel', 'coolantLevel', 'oilLevel']:
                agg_dict[col] = 'min'  # Más conservador
            else:
                agg_dict[col] = 'mean'
        
        df_resampleado = df.resample(frecuencia).agg(agg_dict)
        df_resampleado = df_resampleado.interpolate()
        
        return df_resampleado.reset_index()


class DiagnosticoAutomatico:
    """Diagnóstico automático de problemas del vehículo"""
    
    UMBRALES = {
        'vibracion_critica': 0.8,
        'vibracion_alta': 0.5,
        'presion_baja': 1.8,
        'presion_muy_baja': 1.6,
        'aceite_bajo': 30,
        'aceite_muy_bajo': 20,
        'temperatura_alta': 110,
        'temperatura_critica': 120,
        'consumo_alto': 7.0,
    }
    
    @staticmethod
    def diagnosticar(df):
        """Realizar diagnóstico automático completo"""
        diagnosticos = {
            'criticos': [],
            'advertencias': [],
            'info': [],
            'recomendaciones': [],
            'salud_general': 100,
            'fecha_diagnostico': datetime.now().isoformat(),
        }
        
        # 1. VIBRACIONES
        if 'vibracionMagnitud' in df.columns:
            vibr_max = df['vibracionMagnitud'].max()
            vibr_media = df['vibracionMagnitud'].mean()
            
            if vibr_max > DiagnosticoAutomatico.UMBRALES['vibracion_critica']:
                diagnosticos['criticos'].append({
                    'codigo': 'VIBR_CRITICA',
                    'descripcion': f'Vibraciones anómalas detectadas ({vibr_max:.3f}g)',
                    'causa_probable': [
                        'Desbalanceo cigüeñal',
                        'Bujía/bobina defectuosa',
                        'Desgaste motor avanzado'
                    ],
                    'accion': 'REVISAR CON URGENCIA'
                })
                diagnosticos['salud_general'] -= 30
            
            elif vibr_max > DiagnosticoAutomatico.UMBRALES['vibracion_alta']:
                diagnosticos['advertencias'].append({
                    'codigo': 'VIBR_ALTA',
                    'descripcion': f'Vibraciones elevadas ({vibr_max:.3f}g)',
                    'causa_probable': [
                        'Desgaste neumáticos',
                        'Problema suspensión',
                        'Embrague DSG7 desgastado'
                    ],
                    'accion': 'Revisar en próxima revisión'
                })
                diagnosticos['salud_general'] -= 15
        
        # 2. PRESIÓN NEUMÁTICOS
        for presion_col in ['tirePressureLF', 'tirePressureRF', 'tirePressureLR', 'tirePressureRR']:
            if presion_col in df.columns:
                presion_media = df[presion_col].mean()
                presion_min = df[presion_col].min()
                nombre_rueda = presion_col.replace('tirePressure', '')
                
                if presion_min < DiagnosticoAutomatico.UMBRALES['presion_muy_baja']:
                    diagnosticos['criticos'].append({
                        'codigo': 'PRESION_CRITICA',
                        'descripcion': f'Presión neumático {nombre_rueda}: {presion_min:.2f} bar',
                        'causa_probable': ['Pinchazo', 'Válvula defectuosa'],
                        'accion': 'REVISAR INMEDIATAMENTE'
                    })
                    diagnosticos['salud_general'] -= 25
                
                elif presion_min < DiagnosticoAutomatico.UMBRALES['presion_baja']:
                    diagnosticos['advertencias'].append({
                        'codigo': 'PRESION_BAJA',
                        'descripcion': f'Presión neumático {nombre_rueda}: {presion_min:.2f} bar',
                        'causa_probable': ['Pinchazo lento', 'Desgaste normal'],
                        'accion': 'Verificar presión pronto'
                    })
                    diagnosticos['salud_general'] -= 10
        
        # 3. ACEITE
        if 'oilLevel' in df.columns:
            aceite_min = df['oilLevel'].min()
            
            if aceite_min < DiagnosticoAutomatico.UMBRALES['aceite_muy_bajo']:
                diagnosticos['criticos'].append({
                    'codigo': 'ACEITE_BAJO',
                    'descripcion': f'Nivel de aceite muy bajo: {aceite_min:.1f}%',
                    'causa_probable': ['Fuga de aceite', 'Consumo anormal'],
                    'accion': 'LLENAR INMEDIATAMENTE'
                })
                diagnosticos['salud_general'] -= 25
            
            elif aceite_min < DiagnosticoAutomatico.UMBRALES['aceite_bajo']:
                diagnosticos['advertencias'].append({
                    'codigo': 'ACEITE_BAJO',
                    'descripcion': f'Nivel de aceite bajo: {aceite_min:.1f}%',
                    'causa_probable': ['Consumo normal', 'Próxima revisión'],
                    'accion': 'Llenar aceite pronto'
                })
                diagnosticos['salud_general'] -= 5
        
        # 4. TEMPERATURA
        if 'coolantTemp' in df.columns:
            temp_max = df['coolantTemp'].max()
            
            if temp_max > DiagnosticoAutomatico.UMBRALES['temperatura_critica']:
                diagnosticos['criticos'].append({
                    'codigo': 'TEMP_CRITICA',
                    'descripcion': f'Temperatura motor crítica: {temp_max:.1f}°C',
                    'causa_probable': ['Sistema refrigeración fallido', 'Termostato pegado'],
                    'accion': 'APAGAR MOTOR INMEDIATAMENTE'
                })
                diagnosticos['salud_general'] -= 30
            
            elif temp_max > DiagnosticoAutomatico.UMBRALES['temperatura_alta']:
                diagnosticos['advertencias'].append({
                    'codigo': 'TEMP_ALTA',
                    'descripcion': f'Temperatura motor elevada: {temp_max:.1f}°C',
                    'causa_probable': ['Conducción agresiva', 'Refrigeración lenta'],
                    'accion': 'Revisar sistema refrigeración'
                })
                diagnosticos['salud_general'] -= 10
        
        # 5. CONSUMO
        if 'consumoInstantaneo' in df.columns:
            consumo_medio = df['consumoInstantaneo'].mean()
            
            if consumo_medio > DiagnosticoAutomatico.UMBRALES['consumo_alto']:
                diagnosticos['advertencias'].append({
                    'codigo': 'CONSUMO_ALTO',
                    'descripcion': f'Consumo elevado: {consumo_medio:.2f} L/100km (oficial: 4.8)',
                    'causa_probable': [
                        'Inyectores sucios',
                        'Filtro aire obstruido',
                        'Termostato defectuoso',
                        'Presión neumáticos baja'
                    ],
                    'accion': 'Revisar inyectores e inyección'
                })
                diagnosticos['salud_general'] -= 5
        
        # 6. EFICIENCIA DSG7
        if 'rpm' in df.columns and 'speed' in df.columns:
            # Detectar cambios de marcha anómalos
            rpm_cambios = np.abs(np.diff(df['rpm'].values))
            cambios_bruscos = (rpm_cambios > 1500).sum()
            
            if cambios_bruscos > len(df) * 0.1:  # >10% cambios bruscos
                diagnosticos['advertencias'].append({
                    'codigo': 'DSG_ANOMALIA',
                    'descripcion': f'Cambios de marcha anómalos detectados',
                    'causa_probable': ['Embrague desgastado', 'Sensores DSG'],
                    'accion': 'Revisar transmisión DSG7'
                })
                diagnosticos['salud_general'] -= 8
        
        # Asegurar que la salud no sea negativa
        diagnosticos['salud_general'] = max(0, diagnosticos['salud_general'])
        
        # Generar recomendaciones finales
        DiagnosticoAutomatico._generar_recomendaciones(diagnosticos)
        
        return diagnosticos
    
    @staticmethod
    def _generar_recomendaciones(diagnosticos):
        """Generar recomendaciones basadas en diagnósticos"""
        salud = diagnosticos['salud_general']
        
        if diagnosticos['criticos']:
            diagnosticos['recomendaciones'].append({
                'prioridad': 'CRITICA',
                'accion': 'REVISAR INMEDIATAMENTE CON MECANICO',
                'razon': f"Se detectaron {len(diagnosticos['criticos'])} problemas críticos"
            })
        
        if salud < 30:
            diagnosticos['recomendaciones'].append({
                'prioridad': 'ALTA',
                'accion': 'Agendar revisión completa del vehículo',
                'razon': f'Salud del vehículo en {salud}% (bajo)'
            })
        elif salud < 60:
            diagnosticos['recomendaciones'].append({
                'prioridad': 'MEDIA',
                'accion': 'Revisar en próximas 2 semanas',
                'razon': f'Salud del vehículo en {salud}% (moderada)'
            })
        
        if not diagnosticos['criticos'] and not diagnosticos['advertencias']:
            diagnosticos['recomendaciones'].append({
                'prioridad': 'BAJA',
                'accion': 'Continuar monitoreo normal',
                'razon': 'Vehículo en buen estado'
            })


class GemeloDigitalAvanzado:
    """Gemelo digital mejorado con todas las validaciones"""
    
    def __init__(self, archivo_excel):
        self.archivo = archivo_excel
        self.df = None
        self.df_limpio = None
        self.df_filtrado = None
        self.df_agregado = None
        self.diagnosticos = None
        self.estadisticas_limpieza = None
        
        self.cargar_datos()
    
    def cargar_datos(self):
        """Cargar datos del Excel"""
        try:
            self.df = pd.read_excel(self.archivo, sheet_name='OBD2 Data')
            print(f"✅ Datos cargados: {len(self.df)} registros")
        except Exception as e:
            print(f"❌ Error cargando Excel: {e}")
            return False
        return True
    
    def procesar_datos(self):
        """Procesar datos: validar, filtrar, agregar"""
        print("\n" + "="*60)
        print("🔧 PROCESANDO DATOS")
        print("="*60)
        
        # 1. VALIDACIÓN Y LIMPIEZA
        print("\n1️⃣ Validación y limpieza...")
        self.df_limpio, self.estadisticas_limpieza = ValidadorDatos.limpiar_datos(self.df)
        print(f"   ✅ Registros válidos: {self.estadisticas_limpieza['registros_finales']}")
        print(f"   ✅ Outliers eliminados: {self.estadisticas_limpieza['outliers_eliminados']}")
        print(f"   ✅ Datos válidos: {self.estadisticas_limpieza['porcentaje_valido']:.1f}%")
        
        # 2. FILTRO KALMAN
        print("\n2️⃣ Aplicando filtro Kalman...")
        self.df_filtrado = ValidadorDatos.aplicar_filtro_kalman(self.df_limpio)
        print(f"   ✅ Filtro Kalman aplicado (suavizado de ruido sensor)")
        
        # 3. AGREGACIÓN TEMPORAL
        print("\n3️⃣ Agregación temporal...")
        self.df_agregado = AgregadorTemporal.agregar_por_intervalo(self.df_filtrado, intervalo_segundos=5)
        print(f"   ✅ Datos agregados: {len(self.df_agregado)} registros (cada 5 segundos)")
        print(f"   ✅ Compresión: {len(self.df_filtrado)}/{len(self.df_agregado)} = {len(self.df_filtrado)/len(self.df_agregado):.1f}x")
        
        # 4. DIAGNÓSTICO AUTOMÁTICO
        print("\n4️⃣ Diagnóstico automático...")
        self.diagnosticos = DiagnosticoAutomatico.diagnosticar(self.df_filtrado)
        print(f"   ✅ Problemas críticos: {len(self.diagnosticos['criticos'])}")
        print(f"   ✅ Advertencias: {len(self.diagnosticos['advertencias'])}")
        print(f"   ✅ Salud general: {self.diagnosticos['salud_general']}/100")
    
    def crear_simulacion_3d_avanzada(self):
        """Crear simulación 3D real del vehículo"""
        print("\n" + "="*60)
        print("🚗 CREANDO SIMULACIÓN 3D AVANZADA")
        print("="*60)
        
        # Usar datos agregados para mejor rendimiento
        df = self.df_agregado if self.df_agregado is not None else self.df_filtrado
        
        fig = go.Figure()
        
        # 1. CARROCERÍA
        print("1️⃣ Dibujando carrocería...")
        
        # Puntos clave del Škoda Octavia (dimensiones reales: 4.7m x 1.8m x 1.5m)
        # Estructura básica del vehículo
        carroceria_x = [0, 4.7, 4.7, 0, 0, 0, 4.7, 4.7, 0]
        carroceria_y = [0, 0, 1.8, 1.8, 0, 0, 0, 1.8, 1.8]
        carroceria_z = [0.5, 0.5, 0.5, 0.5, 0.5, 1.5, 1.5, 1.5, 1.5]
        
        fig.add_trace(go.Scatter3d(
            x=carroceria_x, y=carroceria_y, z=carroceria_z,
            mode='lines+markers',
            name='Carrocería',
            line=dict(color='blue', width=4),
            marker=dict(size=8)
        ))
        
        # 2. RUEDAS (DINÁMICAS según presión)
        print("2️⃣ Agregando ruedas con presión dinámica...")
        
        presiones = {
            'LF': df['tirePressureLF'].iloc[-1] if 'tirePressureLF' in df.columns else 2.25,
            'RF': df['tirePressureRF'].iloc[-1] if 'tirePressureRF' in df.columns else 2.25,
            'LR': df['tirePressureLR'].iloc[-1] if 'tirePressureLR' in df.columns else 2.25,
            'RR': df['tirePressureRR'].iloc[-1] if 'tirePressureRR' in df.columns else 2.25,
        }
        
        posiciones_ruedas = {
            'LF': (0.8, 0.2, 0),
            'RF': (3.9, 0.2, 0),
            'LR': (0.8, 1.6, 0),
            'RR': (3.9, 1.6, 0),
        }
        
        for rueda, (x, y, z) in posiciones_ruedas.items():
            presion = presiones[rueda]
            # Color según presión
            if presion < 1.8:
                color = 'red'
                estado = 'CRÍTICO'
            elif presion < 2.0:
                color = 'orange'
                estado = 'BAJO'
            else:
                color = 'green'
                estado = 'OK'
            
            fig.add_trace(go.Scatter3d(
                x=[x], y=[y], z=[z],
                mode='markers+text',
                name=f'Rueda {rueda}',
                marker=dict(size=15, color=color),
                text=[f'{rueda}<br>{presion:.2f}b<br>{estado}'],
                textposition='top center'
            ))
        
        # 3. MOTOR (tamaño dinámico según RPM)
        print("3️⃣ Agregando motor con indicador RPM...")
        
        rpm = df['rpm'].iloc[-1] if 'rpm' in df.columns else 1000
        tamaño_motor = 5 + (rpm / 1000) * 2  # Tamaño proporcional a RPM
        
        # Color según estado RPM
        if rpm > 6500:
            color_motor = 'darkred'
            estado_rpm = 'PELIGRO'
        elif rpm > 5000:
            color_motor = 'orange'
            estado_rpm = 'ALTO'
        else:
            color_motor = 'green'
            estado_rpm = 'NORMAL'
        
        fig.add_trace(go.Scatter3d(
            x=[2.35], y=[0.9], z=[1.2],
            mode='markers+text',
            name='Motor',
            marker=dict(size=tamaño_motor, color=color_motor, opacity=0.7),
            text=[f'{int(rpm)} RPM<br>{estado_rpm}'],
            textposition='top center'
        ))
        
        # 4. INDICADORES DE ESTADO
        print("4️⃣ Agregando indicadores de estado...")
        
        # Temperatura
        temp = df['coolantTemp'].iloc[-1] if 'coolantTemp' in df.columns else 90
        if temp > 110:
            color_temp = 'red'
        elif temp > 95:
            color_temp = 'orange'
        else:
            color_temp = 'lightblue'
        
        fig.add_trace(go.Scatter3d(
            x=[2.35], y=[0.3], z=[0.8],
            mode='markers+text',
            name='Temperatura',
            marker=dict(size=12, color=color_temp),
            text=[f'{temp:.0f}°C'],
            textposition='top center'
        ))
        
        # Consumo
        consumo = df['consumoInstantaneo'].iloc[-1] if 'consumoInstantaneo' in df.columns else 5.0
        if consumo > 7:
            color_consumo = 'red'
        elif consumo > 5.5:
            color_consumo = 'orange'
        else:
            color_consumo = 'green'
        
        fig.add_trace(go.Scatter3d(
            x=[2.35], y=[1.5], z=[0.8],
            mode='markers+text',
            name='Consumo',
            marker=dict(size=12, color=color_consumo),
            text=[f'{consumo:.1f}L/100km'],
            textposition='top center'
        ))
        
        # 5. VIBRACIONES (nube de puntos)
        print("5️⃣ Agregando indicador de vibraciones...")
        
        if 'vibracionMagnitud' in df.columns:
            vibraciones = df['vibracionMagnitud'].values[-50:]  # Últimas 50 lecturas
            
            # Crear pequeña nube de puntos alrededor del motor
            np.random.seed(42)
            cloud_x = 2.35 + np.random.normal(0, 0.1, len(vibraciones)) * (vibraciones / 0.5)
            cloud_y = 0.9 + np.random.normal(0, 0.1, len(vibraciones)) * (vibraciones / 0.5)
            cloud_z = 1.2 + np.random.normal(0, 0.1, len(vibraciones)) * (vibraciones / 0.5)
            
            fig.add_trace(go.Scatter3d(
                x=cloud_x, y=cloud_y, z=cloud_z,
                mode='markers',
                name='Vibraciones',
                marker=dict(
                    size=3,
                    color=vibraciones,
                    colorscale='YlOrRd',
                    showscale=True,
                    colorbar=dict(title='Vibración (g)')
                ),
                text=[f'{v:.3f}g' for v in vibraciones],
                hoverinfo='text'
            ))
        
        # Configurar layout
        fig.update_layout(
            title='🚗 Simulación 3D Real - Škoda Octavia 1.5 TSI 2024',
            scene=dict(
                xaxis=dict(title='Largo (m)', range=[0, 5]),
                yaxis=dict(title='Ancho (m)', range=[0, 2]),
                zaxis=dict(title='Altura (m)', range=[0, 2]),
                camera=dict(eye=dict(x=1.5, y=-2, z=1.2))
            ),
            height=800,
            template='plotly_dark',
            showlegend=True
        )
        
        fig.write_html('gemelo_digital_vehiculo_3d_avanzado.html')
        print("✅ Simulación 3D guardada: gemelo_digital_vehiculo_3d_avanzado.html")
        
        return fig
    
    def crear_diagnostico_visual(self):
        """Crear visualización del diagnóstico automático"""
        print("\n" + "="*60)
        print("🔍 CREANDO DASHBOARD DE DIAGNÓSTICO")
        print("="*60)
        
        diag = self.diagnosticos
        df = self.df_agregado if self.df_agregado is not None else self.df_filtrado
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                f"🏥 Salud General: {diag['salud_general']}/100",
                '⚠️ Problemas Detectados',
                '📊 Parámetros Críticos',
                '💊 Recomendaciones'
            ),
            specs=[
                [{'type': 'indicator'}, {'type': 'table'}],
                [{'type': 'scatter'}, {'type': 'table'}]
            ]
        )
        
        # 1. Indicador de salud
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=diag['salud_general'],
                title="Salud",
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkgreen" if diag['salud_general'] > 70 else "orange" if diag['salud_general'] > 40 else "red"},
                    'steps': [
                        {'range': [0, 40], 'color': "lightcoral"},
                        {'range': [40, 70], 'color': "lightyellow"},
                        {'range': [70, 100], 'color': "lightgreen"}
                    ]
                }
            ),
            row=1, col=1
        )
        
        # 2. Tabla de problemas
        problemas_data = []
        for p in diag['criticos'][:5]:  # Primeros 5
            problemas_data.append([p['codigo'], f"🔴 {p['descripcion']}", p['accion']])
        
        for p in diag['advertencias'][:5]:
            problemas_data.append([p['codigo'], f"🟡 {p['descripcion']}", p['accion']])
        
        fig.add_trace(
            go.Table(
                header=dict(values=['Código', 'Problema', 'Acción']),
                cells=dict(values=[
                    [x[0] for x in problemas_data] if problemas_data else [''],
                    [x[1] for x in problemas_data] if problemas_data else ['Sin problemas'],
                    [x[2] for x in problemas_data] if problemas_data else ['Monitor']
                ])
            ),
            row=1, col=2
        )
        
        # 3. Gráfico de parámetros críticos
        if 'coolantTemp' in df.columns and 'oilLevel' in df.columns:
            fig.add_trace(
                go.Scatter(
                    y=df['coolantTemp'].tail(100),
                    mode='lines',
                    name='Temperatura',
                    line=dict(color='red')
                ),
                row=2, col=1
            )
        
        # 4. Tabla de recomendaciones
        rec_data = []
        for r in diag['recomendaciones']:
            rec_data.append([r['prioridad'], r['accion']])
        
        fig.add_trace(
            go.Table(
                header=dict(values=['Prioridad', 'Acción']),
                cells=dict(values=[
                    [x[0] for x in rec_data] if rec_data else [''],
                    [x[1] for x in rec_data] if rec_data else ['En buen estado']
                ])
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=900, template='plotly_dark', showlegend=False)
        fig.write_html('gemelo_digital_diagnostico_avanzado.html')
        print("✅ Diagnóstico guardado: gemelo_digital_diagnostico_avanzado.html")
    
    def generar_reporte(self):
        """Generar reporte JSON completo"""
        print("\n" + "="*60)
        print("📄 GENERANDO REPORTE")
        print("="*60)
        
        reporte = {
            'fecha': datetime.now().isoformat(),
            'vehiculo': 'Škoda Octavia 1.5 TSI 2024',
            'archivo': str(self.archivo),
            'procesamiento': {
                'estadisticas_limpieza': self.estadisticas_limpieza,
                'registros_procesados': len(self.df_filtrado),
                'registros_agregados': len(self.df_agregado),
            },
            'diagnosticos': self.diagnosticos,
            'parametros_finales': {
                'rpm': float(self.df_filtrado['rpm'].iloc[-1]) if 'rpm' in self.df_filtrado.columns else None,
                'velocidad': float(self.df_filtrado['speed'].iloc[-1]) if 'speed' in self.df_filtrado.columns else None,
                'consumo': float(self.df_filtrado['consumoInstantaneo'].iloc[-1]) if 'consumoInstantaneo' in self.df_filtrado.columns else None,
                'temperatura': float(self.df_filtrado['coolantTemp'].iloc[-1]) if 'coolantTemp' in self.df_filtrado.columns else None,
            }
        }
        
        ruta_reporte = 'reporte_obd2_avanzado.json'
        with open(ruta_reporte, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Reporte guardado: {ruta_reporte}")
        
        # Mostrar resumen
        print(f"\n📊 RESUMEN:")
        print(f"   Salud General: {self.diagnosticos['salud_general']}/100")
        print(f"   Problemas Críticos: {len(self.diagnosticos['criticos'])}")
        print(f"   Advertencias: {len(self.diagnosticos['advertencias'])}")
    
    def ejecutar_completo(self):
        """Ejecutar análisis completo"""
        print("\n" + "█"*60)
        print("█  GEMELO DIGITAL AVANZADO - ANÁLISIS COMPLETO")
        print("█"*60)
        
        self.procesar_datos()
        self.crear_simulacion_3d_avanzada()
        self.crear_diagnostico_visual()
        self.generar_reporte()
        
        print("\n" + "█"*60)
        print("█  ✅ ANÁLISIS COMPLETADO")
        print("█"*60 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python gemelo_digital_avanzado.py archivo.xlsx")
        sys.exit(1)
    
    archivo = sys.argv[1]
    
    if not Path(archivo).exists():
        print(f"❌ Archivo no encontrado: {archivo}")
        sys.exit(1)
    
    gemelo = GemeloDigitalAvanzado(archivo)
    gemelo.ejecutar_completo()
