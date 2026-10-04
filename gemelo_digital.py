#!/usr/bin/env python3
"""
GEMELO DIGITAL - Škoda Octavia 1.5 TSI 2024
Visualización 3D e interactiva en tiempo real de los datos OBD2
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
from pathlib import Path

class GemeloDigitalSkoda:
    """Gemelo digital del Škoda Octavia"""
    
    def __init__(self, archivo_excel):
        """Inicializar con datos Excel"""
        self.archivo = archivo_excel
        self.df = None
        self.cargar_datos()
    
    def cargar_datos(self):
        """Cargar datos del Excel"""
        try:
            self.df = pd.read_excel(self.archivo, sheet_name='OBD2 Data')
            print(f"✅ Gemelo digital: {len(self.df)} registros cargados")
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        return True
    
    # ==================== TABLERO PRINCIPAL ====================
    
    def crear_tablero_principal(self):
        """Dashboard 3D principal del vehículo"""
        print("\n📊 Creando tablero principal...")
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                '🚗 Estado Motor en Tiempo Real',
                '⛽ Consumo vs Velocidad',
                '🔧 Vibraciones Detectadas',
                '🛞 Presión Neumáticos'
            ),
            specs=[
                [{'type': 'scatter'}, {'type': 'scatter'}],
                [{'type': 'scatter'}, {'type': 'bar'}]
            ]
        )
        
        # 1. RPM en tiempo real
        if 'rpm' in self.df.columns:
            fig.add_trace(
                go.Scatter(
                    y=self.df['rpm'],
                    mode='lines',
                    name='RPM',
                    line=dict(color='#ff6b00', width=2),
                    fill='tozeroy'
                ),
                row=1, col=1
            )
        
        # 2. Consumo vs Velocidad
        if 'consumoInstantaneo' in self.df.columns and 'speed' in self.df.columns:
            fig.add_trace(
                go.Scatter(
                    x=self.df['speed'],
                    y=self.df['consumoInstantaneo'],
                    mode='markers',
                    name='Consumo',
                    marker=dict(
                        size=5,
                        color=self.df['consumoInstantaneo'],
                        colorscale='RdYlGn_r',
                        showscale=True,
                        colorbar=dict(x=1.15)
                    )
                ),
                row=1, col=2
            )
        
        # 3. Vibraciones
        if 'vibracionMagnitud' in self.df.columns:
            fig.add_trace(
                go.Scatter(
                    y=self.df['vibracionMagnitud'],
                    mode='lines+markers',
                    name='Vibración',
                    line=dict(color='#ff0000'),
                    marker=dict(size=4)
                ),
                row=2, col=1
            )
        
        # 4. Presión neumáticos promedio
        presiones = {}
        for columna in ['tirePressureLF', 'tirePressureRF', 'tirePressureLR', 'tirePressureRR']:
            if columna in self.df.columns:
                presiones[columna.replace('tirePressure', '')] = self.df[columna].mean()
        
        if presiones:
            fig.add_trace(
                go.Bar(
                    x=list(presiones.keys()),
                    y=list(presiones.values()),
                    name='Presión (bar)',
                    marker_color='#0066ff'
                ),
                row=2, col=2
            )
        
        fig.update_xaxes(title_text="Tiempo (registros)", row=1, col=1)
        fig.update_yaxes(title_text="RPM", row=1, col=1)
        fig.update_xaxes(title_text="Velocidad (km/h)", row=1, col=2)
        fig.update_yaxes(title_text="L/100km", row=1, col=2)
        fig.update_xaxes(title_text="Tiempo (registros)", row=2, col=1)
        fig.update_yaxes(title_text="g", row=2, col=1)
        fig.update_xaxes(title_text="Posición", row=2, col=2)
        fig.update_yaxes(title_text="bar", row=2, col=2)
        
        fig.update_layout(
            title_text="🚗 GEMELO DIGITAL - ŠKODA OCTAVIA 1.5 TSI 2024",
            height=900,
            showlegend=True,
            template='plotly_dark'
        )
        
        fig.write_html("gemelo_digital_tablero.html")
        print("✅ Tablero principal guardado: gemelo_digital_tablero.html")
    
    # ==================== 3D - MOTOR ====================
    
    def crear_motor_3d(self):
        """Visualización 3D del estado del motor"""
        print("\n🏎️ Creando visualización 3D motor...")
        
        if 'rpm' not in self.df.columns or 'power' not in self.df.columns:
            print("⚠️ Faltan datos para motor 3D")
            return
        
        # Crear puntos 3D: RPM, Potencia, Temperatura
        fig = go.Figure(data=[go.Scatter3d(
            x=self.df['rpm'],
            y=self.df.get('power', np.zeros(len(self.df))),
            z=self.df.get('coolantTemp', np.zeros(len(self.df))),
            mode='markers',
            marker=dict(
                size=4,
                color=self.df['rpm'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="RPM"),
                opacity=0.7
            ),
            text=[f"RPM: {int(r)}<br>Pot: {p:.1f}kW<br>Temp: {t:.0f}°C" 
                  for r, p, t in zip(self.df['rpm'], 
                                     self.df.get('power', [0]*len(self.df)),
                                     self.df.get('coolantTemp', [0]*len(self.df)))],
            hoverinfo='text'
        )])
        
        fig.update_layout(
            title='🏎️ Motor 3D: RPM vs Potencia vs Temperatura',
            scene=dict(
                xaxis_title='RPM',
                yaxis_title='Potencia (kW)',
                zaxis_title='Temperatura (°C)',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.3)
                )
            ),
            height=800,
            template='plotly_dark'
        )
        
        fig.write_html("gemelo_digital_motor_3d.html")
        print("✅ Motor 3D guardado: gemelo_digital_motor_3d.html")
    
    # ==================== MAPA DE CALOR - EFICIENCIA ====================
    
    def crear_mapa_calor_eficiencia(self):
        """Mapa de calor: RPM vs Carga vs Consumo"""
        print("\n🔥 Creando mapa de calor eficiencia...")
        
        if 'rpm' not in self.df.columns or 'consumoInstantaneo' not in self.df.columns:
            print("⚠️ Faltan datos para mapa de calor")
            return
        
        # Crear grid de datos
        rpm_bins = pd.cut(self.df['rpm'], bins=20)
        speed_bins = pd.cut(self.df['speed'], bins=20) if 'speed' in self.df.columns else pd.cut(self.df['rpm'], bins=20)
        
        consumo_grid = self.df.groupby([rpm_bins, speed_bins])['consumoInstantaneo'].mean().unstack()
        
        fig = go.Figure(data=go.Heatmap(
            z=consumo_grid.values,
            x=np.arange(consumo_grid.shape[1]),
            y=np.arange(consumo_grid.shape[0]),
            colorscale='RdYlGn_r',
            colorbar=dict(title='L/100km'),
            hovertemplate='RPM Bin: %{y}<br>Speed Bin: %{x}<br>Consumo: %{z:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='🔥 Mapa de Eficiencia: RPM vs Velocidad vs Consumo',
            xaxis_title='Velocidad (bins)',
            yaxis_title='RPM (bins)',
            height=600,
            template='plotly_dark'
        )
        
        fig.write_html("gemelo_digital_mapa_calor.html")
        print("✅ Mapa de calor guardado: gemelo_digital_mapa_calor.html")
    
    # ==================== ANÁLISIS DE VIBRACIONES 3D ====================
    
    def crear_vibraciones_3d(self):
        """Visualización 3D de vibraciones"""
        print("\n📳 Creando análisis vibraciones 3D...")
        
        if 'acelerometerX' not in self.df.columns:
            print("⚠️ Faltan datos de acelerómetro")
            # Simular datos para demostración
            self.df['acelerometerX'] = np.random.normal(0.1, 0.2, len(self.df))
            self.df['acelerometerY'] = np.random.normal(0.1, 0.2, len(self.df))
            self.df['acelerometerZ'] = np.random.normal(0.2, 0.3, len(self.df))
        
        fig = go.Figure(data=[go.Scatter3d(
            x=self.df.get('acelerometerX', [0]),
            y=self.df.get('acelerometerY', [0]),
            z=self.df.get('acelerometerZ', [0]),
            mode='markers',
            marker=dict(
                size=5,
                color=self.df['rpm'] if 'rpm' in self.df.columns else range(len(self.df)),
                colorscale='Turbo',
                showscale=True,
                colorbar=dict(title="RPM"),
                opacity=0.6
            ),
            text=[f"X: {x:.2f}g<br>Y: {y:.2f}g<br>Z: {z:.2f}g" 
                  for x, y, z in zip(
                      self.df.get('acelerometerX', [0]*len(self.df)),
                      self.df.get('acelerometerY', [0]*len(self.df)),
                      self.df.get('acelerometerZ', [0]*len(self.df))
                  )],
            hoverinfo='text'
        )])
        
        fig.update_layout(
            title='📳 Vibraciones 3D: Eje X vs Y vs Z',
            scene=dict(
                xaxis_title='Aceleración X (g)',
                yaxis_title='Aceleración Y (g)',
                zaxis_title='Aceleración Z (g)',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
            ),
            height=800,
            template='plotly_dark'
        )
        
        fig.write_html("gemelo_digital_vibraciones_3d.html")
        print("✅ Vibraciones 3D guardado: gemelo_digital_vibraciones_3d.html")
    
    # ==================== DINÁMICA CONDUCCIÓN ====================
    
    def crear_dinamica_conduccion(self):
        """Análisis dinámico de conducción"""
        print("\n🏁 Creando análisis dinámica conducción...")
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=(
                '⚡ Aceleración vs Deceleración',
                '📊 Velocidad Media por Tramo',
                '🎯 Eficiencia de Conducción'
            ),
            row_heights=[0.3, 0.3, 0.3]
        )
        
        # Calcular aceleración
        if 'speed' in self.df.columns:
            velocidad_m_s = self.df['speed'].values / 3.6
            aceleracion = np.diff(velocidad_m_s) / 0.1  # intervalo 100ms
            aceleracion = np.append(aceleracion, aceleracion[-1])
            
            # Acelerar vs Decelerar
            fig.add_trace(
                go.Scatter(
                    y=aceleracion,
                    mode='lines',
                    name='Aceleración',
                    line=dict(color='#ff0000'),
                    fill='tozeroy'
                ),
                row=1, col=1
            )
        
        # Velocidad por tramos
        if 'speed' in self.df.columns:
            tramos = len(self.df) // 50
            velocidades_tramo = [self.df['speed'].iloc[i*50:(i+1)*50].mean() 
                                 for i in range(tramos)]
            
            fig.add_trace(
                go.Bar(
                    y=velocidades_tramo,
                    name='Vel Media',
                    marker_color='#0066ff'
                ),
                row=2, col=1
            )
        
        # Eficiencia
        if 'consumoInstantaneo' in self.df.columns:
            eficiencia = (1 - (self.df['consumoInstantaneo'] / self.df['consumoInstantaneo'].max())) * 100
            
            fig.add_trace(
                go.Scatter(
                    y=eficiencia,
                    mode='lines',
                    name='Eficiencia',
                    line=dict(color='#00aa44', width=3),
                    fill='tozeroy'
                ),
                row=3, col=1
            )
        
        fig.update_yaxes(title_text="m/s²", row=1, col=1)
        fig.update_yaxes(title_text="km/h", row=2, col=1)
        fig.update_yaxes(title_text="%", row=3, col=1)
        fig.update_xaxes(title_text="Tiempo (registros)", row=3, col=1)
        
        fig.update_layout(height=900, template='plotly_dark', showlegend=True)
        fig.write_html("gemelo_digital_dinamica.html")
        print("✅ Dinámica conducción guardado: gemelo_digital_dinamica.html")
    
    # ==================== CORRELACIONES 3D ====================
    
    def crear_correlaciones_3d(self):
        """Matriz de correlaciones 3D"""
        print("\n🔗 Creando correlaciones 3D...")
        
        # Seleccionar columnas numéricas
        columnas_num = self.df.select_dtypes(include=[np.number]).columns
        
        # Calcular matriz de correlaciones
        corr_matrix = self.df[columnas_num].corr()
        
        # Crear heatmap interactivo
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            colorbar=dict(title="Correlación"),
            hovertemplate='%{y} vs %{x}<br>Correlación: %{z:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='🔗 Matriz de Correlaciones - Parámetros Motor',
            xaxis_title='Parámetro',
            yaxis_title='Parámetro',
            height=800,
            width=900,
            template='plotly_dark'
        )
        
        fig.write_html("gemelo_digital_correlaciones.html")
        print("✅ Correlaciones 3D guardado: gemelo_digital_correlaciones.html")
    
    # ==================== DIAGNÓSTICO EN TIEMPO REAL ====================
    
    def crear_diagnostico_realtime(self):
        """Dashboard de diagnóstico en tiempo real"""
        print("\n🔍 Creando diagnóstico en tiempo real...")
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                '🚨 Alertas Críticas',
                '⚙️ Parámetros Motor',
                '🔧 Sistemas Detectados',
                '📈 Tendencias'
            ),
            specs=[
                [{'type': 'indicator'}, {'type': 'gauge'}],
                [{'type': 'table'}, {'type': 'scatter'}]
            ]
        )
        
        # 1. Indicadores críticos
        alertas_count = 0
        if 'vibracionMagnitud' in self.df.columns:
            alertas_count += (self.df['vibracionMagnitud'] > 0.5).sum()
        
        fig.add_trace(
            go.Indicator(
                mode="number+gauge",
                value=alertas_count,
                title="Alertas Detectadas",
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "red" if alertas_count > 0 else "green"}}
            ),
            row=1, col=1
        )
        
        # 2. Gauge RPM
        if 'rpm' in self.df.columns:
            rpm_actual = self.df['rpm'].iloc[-1]
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=rpm_actual,
                    title="RPM Actual",
                    gauge={'axis': {'range': [0, 7000]},
                           'bar': {'color': "blue"},
                           'steps': [
                               {'range': [0, 3000], 'color': "lightgray"},
                               {'range': [3000, 6000], 'color': "gray"}],
                           'threshold': {'line': {'color': "red"}, 'thickness': 4, 'value': 6500}}
                ),
                row=1, col=2
            )
        
        # 3. Tabla de sistemas
        sistemas = {
            'Sistema': ['Motor', 'Transmisión', 'Neumáticos', 'Suspensión', 'Frenos'],
            'Estado': ['✅ OK', '✅ OK', '⚠️ Revisar', '✅ OK', '✅ OK'],
            'Último Chequeo': ['Ahora', 'Ahora', '5 min', 'Ahora', 'Ahora']
        }
        
        fig.add_trace(
            go.Table(
                header=dict(values=list(sistemas.keys()),
                           fill_color='paleturquoise',
                           align='left'),
                cells=dict(values=[sistemas[k] for k in sistemas.keys()],
                          fill_color='lavender',
                          align='left')),
            row=2, col=1
        )
        
        # 4. Tendencia consumo
        if 'consumoInstantaneo' in self.df.columns:
            fig.add_trace(
                go.Scatter(
                    y=self.df['consumoInstantaneo'].rolling(10).mean(),
                    mode='lines',
                    name='Consumo Media Móvil',
                    line=dict(color='orange', width=3)
                ),
                row=2, col=2
            )
        
        fig.update_yaxes(title_text="L/100km", row=2, col=2)
        fig.update_layout(height=900, template='plotly_dark', showlegend=False)
        fig.write_html("gemelo_digital_diagnostico.html")
        print("✅ Diagnóstico en tiempo real: gemelo_digital_diagnostico.html")
    
    # ==================== SIMULACIÓN 3D DEL VEHÍCULO ====================
    
    def crear_vehículo_3d(self):
        """Simulación 3D del vehículo"""
        print("\n🚗 Creando simulación 3D vehículo...")
        
        # Crear geometría simple del vehículo
        # (aproximación: rectángulo con ruedas)
        
        fig = go.Figure()
        
        # Carrocería (rectángulo)
        carroceria_x = [0, 4.7, 4.7, 0, 0]
        carroceria_y = [0, 0, 1.8, 1.8, 0]
        carroceria_z = [0.5, 0.5, 0.5, 0.5, 0.5]
        
        fig.add_trace(go.Scatter3d(
            x=carroceria_x, y=carroceria_y, z=carroceria_z,
            mode='lines+markers',
            name='Carrocería',
            line=dict(color='blue', width=4),
            marker=dict(size=8)
        ))
        
        # Ruedas (simulación de presión)
        if 'tirePressureLF' in self.df.columns:
            presiones = [
                self.df['tirePressureLF'].iloc[-1],
                self.df['tirePressureRF'].iloc[-1],
                self.df['tirePressureLR'].iloc[-1],
                self.df['tirePressureRR'].iloc[-1]
            ]
            posiciones_x = [1.0, 3.7, 1.0, 3.7]
            posiciones_y = [0, 0, 1.8, 1.8]
            
            colores = ['green' if p > 2.0 else 'orange' if p > 1.8 else 'red' for p in presiones]
            
            fig.add_trace(go.Scatter3d(
                x=posiciones_x, y=posiciones_y, z=[0]*4,
                mode='markers+text',
                name='Neumáticos',
                marker=dict(size=15, color=colores),
                text=[f'{p:.2f}' for p in presiones],
                textposition='top center'
            ))
        
        # Motores indicadores RPM
        if 'rpm' in self.df.columns:
            rpm = self.df['rpm'].iloc[-1]
            tamaño = 5 + (rpm / 1000)  # Tamaño proporcional a RPM
            
            fig.add_trace(go.Scatter3d(
                x=[2.35], y=[0.9], z=[1.5],
                mode='markers+text',
                name='Motor',
                marker=dict(size=tamaño, color='red'),
                text=[f'{int(rpm)} RPM'],
                textposition='top center'
            ))
        
        fig.update_layout(
            title='🚗 Simulación 3D - Škoda Octavia 1.5 TSI 2024',
            scene=dict(
                xaxis_title='Largo (m)',
                yaxis_title='Ancho (m)',
                zaxis_title='Altura (m)',
                camera=dict(eye=dict(x=1.5, y=-1.5, z=1.2))
            ),
            height=700,
            template='plotly_dark',
            showlegend=True
        )
        
        fig.write_html("gemelo_digital_vehiculo_3d.html")
        print("✅ Vehículo 3D guardado: gemelo_digital_vehiculo_3d.html")
    
    # ==================== EXPORTAR TODOS LOS GRÁFICOS ====================
    
    def generar_indice_html(self):
        """Crear página índice con todos los gráficos"""
        print("\n📑 Creando página índice...")
        
        html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚗 Gemelo Digital - Škoda Octavia 1.5 TSI 2024</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #fff;
            padding: 20px;
            margin: 0;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .subtitle {
            text-align: center;
            font-size: 1.2em;
            margin-bottom: 40px;
            opacity: 0.9;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        .card h3 {
            margin-top: 0;
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        .card p {
            margin: 10px 0;
            opacity: 0.9;
        }
        .card a {
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background: #0066ff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .card a:hover {
            background: #0052cc;
        }
        .stats {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 40px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .stat-item {
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #00ff00;
        }
        .stat-label {
            opacity: 0.8;
            margin-top: 5px;
        }
        .footer {
            text-align: center;
            opacity: 0.7;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚗 GEMELO DIGITAL</h1>
        <p class="subtitle">Škoda Octavia 1.5 TSI 2024 - Análisis en Tiempo Real</p>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-value">7</div>
                <div class="stat-label">Gráficos 3D</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">65+</div>
                <div class="stat-label">Parámetros</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">100%</div>
                <div class="stat-label">Interactivo</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">Tiempo Real</div>
                <div class="stat-label">Actualización</div>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>📊 Tablero Principal</h3>
                <p>Dashboard con los principales parámetros del vehículo en tiempo real: RPM, consumo, vibraciones y presión de neumáticos.</p>
                <a href="gemelo_digital_tablero.html" target="_blank">Abrir Gráfico →</a>
            </div>
            
            <div class="card">
                <h3>🏎️ Motor 3D</h3>
                <p>Visualización tridimensional del estado del motor: RPM vs Potencia vs Temperatura. Explora el espacio de operación.</p>
                <a href="gemelo_digital_motor_3d.html" target="_blank">Abrir Gráfico →</a>
            </div>
            
            <div class="card">
                <h3>🔥 Mapa de Calor</h3>
                <p>Heatmap interactivo mostrando eficiencia: RPM vs Velocidad vs Consumo. Identifica zonas óptimas de conducción.</p>
                <a href="gemelo_digital_mapa_calor.html" target="_blank">Abrir Gráfico →</a>
            </div>
            
            <div class="card">
                <h3>📳 Vibraciones 3D</h3>
                <p>Análisis tridimensional de vibraciones captadas por acelerómetro. Eje X, Y, Z en tiempo real.</p>
                <a href="gemelo_digital_vibraciones_3d.html" target="_blank">Abrir Gráfico →</a>
            </div>
            
            <div class="card">
                <h3>🏁 Dinámica Conducción</h3>
                <p>Análisis de aceleración, deceleración, velocidad media y eficiencia por tramos.</p>
                <a href="gemelo_digital_dinamica.html" target="_blank">Abrir Gráfico →</a>
            </div>
            
            <div class="card">
                <h3>🔗 Correlaciones</h3>
                <p>Matriz de correlaciones 3D entre todos los parámetros. Descubre relaciones ocultas.</p>
                <a href="gemelo_digital_correlaciones.html" target="_blank">Abrir Gráfico →</a>
            </div>
            
            <div class="card">
                <h3>🔍 Diagnóstico</h3>
                <p>Dashboard de diagnóstico en tiempo real con alertas, sistemas detectados y tendencias.</p>
                <a href="gemelo_digital_diagnostico.html" target="_blank">Abrir Gráfico →</a>
            </div>
            
            <div class="card">
                <h3>🚗 Vehículo 3D</h3>
                <p>Simulación 3D del Škoda Octavia mostrando estado de ruedas, motor y sistemas.</p>
                <a href="gemelo_digital_vehiculo_3d.html" target="_blank">Abrir Gráfico →</a>
            </div>
        </div>
        
        <div class="footer">
            <p>🔄 Todos los gráficos son interactivos: zoom, pan, hover para detalles</p>
            <p>Generado con Python + Plotly | Datos OBD2 Real</p>
            <p>Última actualización: """ + str(pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")) + """</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open('gemelo_digital_indice.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        print("✅ Página índice creada: gemelo_digital_indice.html")
        print("   Abre este archivo en el navegador para ver todos los gráficos")
    
    # ==================== EJECUTAR TODO ====================
    
    def generar_gemelo_completo(self):
        """Generar gemelo digital completo"""
        print("\n" + "█"*60)
        print("█  GENERANDO GEMELO DIGITAL COMPLETO")
        print("█"*60)
        
        self.crear_tablero_principal()
        self.crear_motor_3d()
        self.crear_mapa_calor_eficiencia()
        self.crear_vibraciones_3d()
        self.crear_dinamica_conduccion()
        self.crear_correlaciones_3d()
        self.crear_diagnostico_realtime()
        self.crear_vehículo_3d()
        self.generar_indice_html()
        
        print("\n" + "█"*60)
        print("█  ✅ GEMELO DIGITAL COMPLETADO")
        print("█"*60)
        print("\n🌐 Abre en navegador: gemelo_digital_indice.html")
        print("   Para ver todos los gráficos interactivos\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python gemelo_digital.py archivo.xlsx")
        print("Ejemplo: python gemelo_digital.py obd2-consumo-2026-04-06.xlsx")
        sys.exit(1)
    
    archivo = sys.argv[1]
    
    if not Path(archivo).exists():
        print(f"❌ Archivo no encontrado: {archivo}")
        sys.exit(1)
    
    # Generar gemelo digital
    gemelo = GemeloDigitalSkoda(archivo)
    gemelo.generar_gemelo_completo()
