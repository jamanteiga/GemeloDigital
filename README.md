# OBD2 Dashboard Škoda Octavia 1.5 TSI 2024 🚗

Dashboard PWA para capturar, analizar y monitorear datos OBD2 en tiempo real desde tu iPhone.

**Características:**
- ✅ Captura datos OBD2 en tiempo real via Bluetooth
- ✅ 65+ parámetros configurables
- ✅ Gráficos dinámicos en tiempo real (RPM, velocidad, potencia, consumo)
- ✅ Análisis de vibraciones con acelerómetro del iPhone
- ✅ Cálculo de consumo total y medio por trayecto
- ✅ Alertas críticas automáticas (presión neumáticos, aceite, temperatura)
- ✅ Diagnóstico manual OBD2 con almacenamiento
- ✅ Exportación a Excel con datos completos
- ✅ Análisis avanzado en Python

## 📋 Requisitos

### Para la PWA (iPhone/iPad):
- iPhone/iPad con iOS 13+
- Adaptador OBD2 Bluetooth (cualquier marca)
- Windows 11 con VS Code para desarrollo

### Para análisis avanzado (Python):
- Python 3.8+
- Librerías: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `plotly`

## 🚀 Instalación

### 1. PWA - Setup inicial

```bash
# En Windows 11 - Descargar archivos
git clone https://github.com/tu-usuario/obd2-dashboard.git
cd obd2-dashboard

# Instalar VS Code si no lo tienes
# https://code.visualstudio.com/

# Abrir el proyecto en VS Code
code .

# Instalar extensión "Live Server" en VS Code
# Buscar "Live Server" en Extensions
```

### 2. Ejecutar en el iPhone

```
# En Windows - Click derecho sobre obd2-app.html
# Open with Live Server
# Se abre en http://localhost:5500

# En Windows - Abrir CMD y obtener IP local
ipconfig

# En iPhone - Abrir Safari
# Ir a http://192.168.x.x:5500
# (reemplazar x.x con tu IP de Windows)

# En iPhone - Safari → Compartir → Añadir a pantalla inicio
# Ahora tienes la PWA instalada como app
```

### 3. Python - Análisis avanzado

```bash
# Instalar dependencias
pip install -r requirements.txt

# 1. ANÁLISIS COMPLETO
python analisis_obd2.py obd2-consumo-2026-04-06.xlsx

# Se generarán:
# - reporte_obd2.json
# - consumo_tiempo_real.html
# - rpm_vs_consumo.html
# - vibraciones_tiempo_real.html
# - velocidad_vs_vibraciones.html

# 2. GEMELO DIGITAL (⭐ Recomendado)
python gemelo_digital.py obd2-consumo-2026-04-06.xlsx

# Se generarán 8 gráficos 3D interactivos:
# - gemelo_digital_indice.html (página principal con todos los gráficos)
# - gemelo_digital_tablero.html
# - gemelo_digital_motor_3d.html
# - gemelo_digital_mapa_calor.html
# - gemelo_digital_vibraciones_3d.html
# - gemelo_digital_dinamica.html
# - gemelo_digital_correlaciones.html
# - gemelo_digital_diagnostico.html
# - gemelo_digital_vehiculo_3d.html
```

## 📖 Guía de uso

### En la PWA:

1. **Conexión**: Click en "Conectar OBD2"
2. **Configuración**: Seleccionar parámetros (ya están preconfigurados)
3. **Grabación**: Click en "Grabar" y conducir
4. **Monitoreo**: Ver gráficos en tiempo real
5. **Descargar**: Click en "Descargar Excel" para obtener datos

### Parámetros disponibles:

**GPS & Localización:**
- Latitud, Longitud, Altitud, Velocidad GPS

**Motor (Škoda Octavia 1.5 TSI 2024):**
- RPM, Velocidad, Potencia (110 kW / 150 CV)
- Temperatura motor, Presión aceite
- Carga motor, Aceleración

**Neumáticos (TPMS):**
- Presión frontal izquierdo (bar)
- Presión frontal derecho (bar)
- Presión trasero izquierdo (bar)
- Presión trasero derecho (bar)

**Vibraciones (Acelerómetro iPhone):**
- Aceleración X, Y, Z (g)
- Magnitud total vibración

**Consumo:**
- Consumo instantáneo (L/100km)
- Consumo total del trayecto
- Velocidad media

**Diagnóstico:**
- Códigos de error OBD2
- Nivel de aceite y refrigerante
- Presión turbo

## 📊 Análisis avanzado con Python

El script `analisis_obd2.py` proporciona:

### Análisis de consumo:
- Consumo medio, mínimo, máximo
- Comparación con oficial WLTP (4.8 L/100km)
- Desviación estándar

### Análisis de vibraciones:
- Magnitud de vibraciones
- Diagnóstico automático de problemas
- Correlación con RPM y velocidad

### Gráficos interactivos:
- Consumo en tiempo real
- RPM vs Consumo (scatter)
- Vibraciones en tiempo real
- Velocidad vs Vibraciones

### Análisis FFT:
- Frecuencias dominantes
- Detección de anomalías periódicas

### Reporte automático:
- JSON con resumen completo
- Alertas detectadas
- Recomendaciones de mantenimiento

## 🔧 Mantenimiento preventivo

El sistema detecta automáticamente:

**Vibración anómala (>0.8 g):**
- ❌ Desbalanceo cigüeñal
- ❌ Bujía/bobina defectuosa
- ❌ Desgaste motor avanzado

**Vibración elevada (0.5-0.8 g):**
- ⚠️ Desgaste neumáticos
- ⚠️ Problema suspensión
- ⚠️ Embrague DSG7 desgastado

**Consumo alto (>5.5 L/100km):**
- Inyectores sucios
- Filtro aire sucio
- Termostato defectuoso

**Presión aceite baja:**
- Fuga de aceite
- Bomba aceite fallando
- Válvulas pegadas

**Presión neumáticos baja:**
- Pinchazo lento
- Válvula defectuosa
- Desgaste irregular

## 📱 Compatibilidad

- ✅ iPhone 8+ con iOS 13+
- ✅ iPad con iOS 13+
- ✅ Android (navegador Chrome)
- ❌ Windows/Mac (se puede acceder pero sin acelerómetro)

## 🐛 Solución de problemas

**"No se conecta OBD2":**
- Verificar que el adaptador esté emparejado en Bluetooth de iOS
- Reiniciar la app
- Reiniciar el adaptador OBD2

**"No aparece acelerómetro":**
- iPhone: iOS 13+ necesario
- iOS 14+: Dar permiso de acceso a movimiento en Configuración
- Algunos dispositivos no tienen acelerómetro

**"Excel no se descarga":**
- Verificar que hay registros grabados
- Usar Safari (no Chrome)
- Comprobar espacio disponible en iPhone

**"Gráficos en Python no aparecen":**
- Verificar que plotly está instalado: `pip install plotly`
- Abrir los ficheros HTML con navegador
- Comprobar que el Excel tiene datos

## 📚 Archivos del proyecto

```
obd2-dashboard/
├── obd2-app.html              # PWA principal
├── analisis_obd2.py           # Script análisis Python
├── requirements.txt           # Dependencias Python
├── README.md                  # Este fichero
├── .gitignore                # Archivos a ignorar en Git
└── data/                      # Carpeta para Excel descargados
    ├── obd2-consumo-*.xlsx
    └── reporte_obd2.json
```

## 🌐 Subir a GitHub

Ver archivo `GITHUB_SETUP.md` para instrucciones completas.

Resumido:
```bash
git init
git add .
git commit -m "Inicial: OBD2 Dashboard Škoda Octavia"
git branch -M main
git remote add origin https://github.com/tu-usuario/obd2-dashboard.git
git push -u origin main
```

## 📝 Especificaciones Škoda Octavia 1.5 TSI 2024

| Parámetro | Valor |
|-----------|-------|
| **Cilindrada** | 1.498 cc |
| **Cilindros** | 4 |
| **Potencia** | 150 CV (110 kW) |
| **Par máximo** | 250 Nm |
| **0-100 km/h** | 8.5 segundos |
| **Velocidad máxima** | 229 km/h |
| **Consumo WLTP** | 4.8 L/100km |
| **Emisiones CO₂** | 110 g/km |
| **Transmisión** | DSG 7 velocidades |
| **Tecnología** | mHEV + Desconexión cilindros |

## 📄 Licencia

MIT License - Libre para uso personal y comercial

## 👨‍💻 Autor

Desarrollado para análisis de datos OBD2 en vehículos Grupo Volkswagen

## 🤝 Contribuciones

Las contribuciones son bienvenidas:

1. Hacer fork del proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📧 Contacto

Para dudas o sugerencias, abre un Issue en GitHub.

---

**Última actualización:** Abril 2026
**Versión:** 2.0 (con análisis de vibraciones)
