#!/usr/bin/env python3
"""
Script de análisis avanzado para datos OBD2 Škoda Octavia 1.5 TSI 2024
Analiza: Consumo, vibraciones, eficiencia, mantenimiento preventivo
Modificado para ejecución directa en Visual Studio Community 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import signal
from scipy.fft import fft, fftfreq
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json
from datetime import datetime
import sys
import os
import glob

class AnalisadorOBD2:
    """Analizador de datos OBD2 Škoda Octavia"""
    
    def __init__(self, archivo_excel):
        """
        Inicializar con fichero Excel de OBD2
        """
        self.archivo = archivo_excel
        self.df = None
        self.resumen = {}
        self.alertas = []
        
        # Cargar datos
        self._cargar_datos()
    
    def _cargar_datos(self):
        """Cargar datos del Excel"""
        try:
            # Forzamos la lectura de la hoja 'OBD2 Data' que genera tu App
            self.df = pd.read_excel(self.archivo, sheet_name='OBD2 Data')
            print(f"✅ Datos cargados: {len(self.df)} registros")
        except Exception as e:
            print(f"❌ Error cargando Excel: {e}")
            return False
        return True
    
    def analizar_consumo(self):
        """Análisis detallado de consumo combustible"""
        print("\n" + "="*60)
        print("📊 ANÁLISIS DE CONSUMO")
        print("="*60)
        
        if 'consumoInstantaneo' not in self.df.columns:
            print("⚠️ Columna de consumo no encontrada")
            return
        
        consumo = self.df['consumoInstantaneo'].dropna()
        self.resumen['consumo'] = {
            'media': consumo.mean(),
            'maximo': consumo.max()
        }
        
        print(f"Consumo medio: {self.resumen['consumo']['media']:.2f} L/100km")
        
        # Comparativa con el oficial del 1.5 TSI (4.8 L/100km)
        if self.resumen['consumo']['media'] > 5.3:
            self.alertas.append(f"⚠️ Consumo elevado (+{(self.resumen['consumo']['media']-4.8):.1f}L sobre oficial)")

    def analizar_vibraciones(self):
        """Análisis de vibraciones mediante acelerómetro"""
        print("\n" + "="*60)
        print("🔧 ANÁLISIS DE VIBRACIONES")
        print("="*60)
        
        if 'vibracionMagnitud' not in self.df.columns:
            print("⚠️ Datos de vibraciones no encontrados")
            return
        
        vibraciones = self.df['vibracionMagnitud'].dropna()
        max_v = vibraciones.max()
        self.resumen['vibraciones'] = {'maximo': max_v}
        
        print(f"Vibración máxima registrada: {max_v:.3f} g")
        
        if max_v > 0.8:
            self.alertas.append("❌ ALERTA CRÍTICA: Vibraciones motor anómalas")
        elif max_v > 0.5:
            self.alertas.append("⚠️ Vibraciones por encima de lo normal")
        else:
            print("✅ Estabilidad del motor: EXCELENTE")

    def generar_graficos_plotly(self):
        """Generar dashboards interactivos HTML"""
        print("\n" + "="*60)
        print("📊 GENERANDO DASHBOARDS INTERACTIVOS")
        print("="*60)
        
        if 'consumoInstantaneo' in self.df.columns:
            fig = px.line(self.df, y='consumoInstantaneo', title="Telemetría de Consumo - Škoda Octavia")
            fig.write_html("consumo_tiempo_real.html")
            print("✅ Archivo creado: consumo_tiempo_real.html")

    def generar_reporte(self):
        """Resumen final en consola"""
        print("\n" + "█"*60)
        print(f"📄 REPORTE FINAL: {self.archivo}")
        print("█"*60)
        if self.alertas:
            for a in self.alertas: print(a)
        else:
            print("✅ Vehículo en estado óptimo.")

    def ejecutar_analisis_completo(self):
        if self.df is None: return
        self.analizar_consumo()
        self.analizar_vibraciones()
        self.generar_graficos_plotly()
        self.generar_reporte()

# ==========================================================
# BLOQUE MODIFICADO PARA VISUAL STUDIO COMMUNITY
# ==========================================================
if __name__ == "__main__":
    # 1. Intentar capturar archivo por argumento (línea de comandos)
    if len(sys.argv) > 1:
        archivo_objetivo = sys.argv[1]
    else:
        # 2. Si pulsas F5 (sin argumentos), buscamos el primer Excel en la carpeta
        print("🔎 Buscando archivos de datos automáticamente...")
        archivos_excel = glob.glob("*.xlsx")
        
        if archivos_excel:
            archivo_objetivo = archivos_excel[0]
            print(f"📂 Archivo detectado: {archivo_objetivo}")
        else:
            print("❌ ERROR: No se encontró ningún archivo .xlsx")
            print("💡 Asegúrate de que el Excel de la App esté en la misma carpeta que este script.")
            # Pausa para que no se cierre la ventana de VS inmediatamente
            input("\nPresiona Enter para salir...")
            sys.exit(1)

    # 3. Ejecutar el análisis
    analizador = AnalisadorOBD2(archivo_objetivo)
    analizador.ejecutar_analisis_completo()
    
    print("\n🚀 Análisis finalizado con éxito.")
    # Mantiene la consola abierta en VS para ver los resultados
    input("Presiona Enter para cerrar...")