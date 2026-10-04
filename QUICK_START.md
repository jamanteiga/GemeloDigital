# 🚀 GUÍA RÁPIDA - OBD2 Dashboard Škoda

## ¿Qué es esto?

Es una **app PWA para iPhone** que:
- 📊 Captura datos OBD2 en tiempo real
- 📱 Mide vibraciones con el acelerómetro
- 📈 Genera gráficos de consumo y eficiencia
- 🔧 Analiza problemas de mantenimiento
- ⚠️ Alerta de problemas críticos

## Instalación (15 minutos)

### 1. En Windows 11

```bash
# Instalar Git
https://git-scm.com/download/win

# Descargar VS Code
https://code.visualstudio.com/

# En VS Code instalar extensión "Live Server"
# (Buscar en extensiones)

# Descargar este proyecto
# Descomprimirlo en una carpeta
# Abrir en VS Code
# Click derecho en obd2-app.html → "Open with Live Server"
```

### 2. En iPhone

```
Safari → http://192.168.x.x:5500
(obtener IP de Windows con: ipconfig)

Safari → Compartir → Añadir a pantalla inicio
(Ahora tienes la app instalada)
```

### 3. Usar la app

```
1. Click "Conectar OBD2"
2. Emparejar adaptador en Bluetooth del iPhone
3. Click "Grabar" y conducir
4. Ver datos en tiempo real
5. Click "Descargar Excel" cuando termines
```

## Análisis en Python (5 minutos)

### 1. Instalar Python

```bash
# Descargar: https://www.python.org/downloads/
# Instalar (marcar "Add Python to PATH")
```

### 2. Instalar librerías

```bash
pip install -r requirements.txt
```

### 3. Analizar datos

```bash
python analisis_obd2.py tu-archivo.xlsx
```

Se genera:
- `reporte_obd2.json` - Resumen completo
- `consumo_tiempo_real.html` - Gráfico consumo
- `rpm_vs_consumo.html` - Relación RPM/consumo
- `vibraciones_tiempo_real.html` - Gráfico vibraciones
- `velocidad_vs_vibraciones.html` - Análisis vibraciones

## Subir a GitHub (10 minutos)

### 1. Crear cuenta GitHub

https://github.com (Sign up)

### 2. Crear repositorio

En GitHub:
- Click **"+"** → **"New repository"**
- Nombre: `obd2-dashboard-skoda`
- Público
- Click "Create repository"

### 3. Subir código

```bash
# En la carpeta del proyecto (CMD)

git init
git add .
git commit -m "Inicial: OBD2 Dashboard Škoda"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/obd2-dashboard-skoda.git
git push -u origin main

# Cuando pida contraseña:
# Usar token de GitHub (Settings → Developer settings → Personal access tokens)
```

### 4. Listo

Tu código está en: https://github.com/TU_USUARIO/obd2-dashboard-skoda

## 🎯 Funcionamiento básico

```
┌─────────────────────────────────────┐
│   iPhone + Adaptador OBD2 Bluetooth  │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│      PWA (obd2-app.html)            │
│  • Captura datos OBD2               │
│  • Mide vibraciones acelerómetro    │
│  • Gráficos en tiempo real          │
│  • Alertas automáticas              │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Descarga Excel (.xlsx)             │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Python (analisis_obd2.py)          │
│  • Análisis profundo                │
│  • Gráficos interactivos            │
│  • Reporte JSON                     │
│  • Diagnóstico automático           │
└─────────────────────────────────────┘
```

## 📊 Datos que captura

### Motor Škoda Octavia 1.5 TSI 2024
- RPM, velocidad, potencia (150 CV)
- Temperatura, presión aceite
- Carga motor, aceleración

### Neumáticos (TPMS)
- Presión de cada rueda (bar)
- Desgaste estimado

### Vibraciones (iPhone)
- Aceleración X, Y, Z (g)
- Magnitud total

### Consumo
- Instantáneo y total (L/100km)
- Velocidad media
- Distancia recorrida

### Diagnóstico
- Códigos de error OBD2
- Nivel de fluidos
- Presión turbo

## ⚠️ Alertas automáticas

**Críticas (🔴):**
- Presión neumático < 1.8 bar
- Nivel aceite < 20%
- Temperatura motor > 110°C
- Vibraciones > 0.8 g

**Advertencias (🟡):**
- Consumo > 5.5 L/100km
- Presión neumático < 2.0 bar
- Vibraciones 0.5-0.8 g

## 🔧 Mantenimiento detecta:

**Vibraciones altas:**
- Desbalanceo cigüeñal
- Bujías defectuosas
- Desgaste motor

**Consumo alto:**
- Inyectores sucios
- Filtro aire sucio
- Termostato fallando

**Presión aceite baja:**
- Fuga de aceite
- Bomba fallando
- Válvulas pegadas

## 📁 Archivos necesarios

```
📦 obd2-dashboard-skoda/
├── 📄 obd2-app.html           ← La app PWA
├── 🐍 analisis_obd2.py        ← Script análisis
├── 📋 requirements.txt         ← Dependencias Python
├── 📖 README.md               ← Documentación completa
├── 🚀 GITHUB_SETUP.md         ← Guía GitHub detallada
├── 🙈 .gitignore              ← Archivos a ignorar
└── 📊 data/                   ← Carpeta para Excel
    └── obd2-*.xlsx            ← Tus datos descargados
```

## 💡 Consejos

1. **Primeras grabaciones:** Haz trayectos cortos (10-20 km) para probar
2. **Acelerómetro iPhone:** En iOS 14+ dar permiso en Configuración
3. **Adaptador OBD2:** Cualquiera Bluetooth funciona (10€ en Amazon)
4. **Análisis:** Espera a tener 3-5 trayectos antes de analizar patrones
5. **Compartir:** GitHub te permite mostrar tu proyecto al mundo

## ❓ Problemas comunes

**"No conecta OBD2"**
- Verificar que esté emparejado en Bluetooth de iOS
- Reiniciar app
- Reiniciar adaptador

**"No funciona acelerómetro"**
- iOS 13+ obligatorio
- Dar permiso en Configuración → Privacidad
- Algunos dispositivos no lo tienen

**"Python no encuentra módulos"**
```bash
pip install -r requirements.txt --upgrade
```

**"No veo gráficos en HTML"**
- Abrir con navegador (no desde fichero local)
- Usar Python: `python -m http.server 8000`

## 📞 Soporte

1. Lee **README.md** completo
2. Lee **GITHUB_SETUP.md** para GitHub
3. Abre **Issue** en GitHub con tu problema
4. Busca en Issues existentes

## 🎯 Próximos pasos

Después de instalar:

1. ✅ Instalar adaptador OBD2 Bluetooth en el coche
2. ✅ Emparejar en Bluetooth del iPhone
3. ✅ Hacer primer trayecto de prueba
4. ✅ Descarga Excel
5. ✅ Analiza con Python
6. ✅ Sube tu proyecto a GitHub
7. ✅ Comparte con amigos

## 📊 Ejemplo de uso real

```
Sábado tarde - Trayecto ciudad 15 km:
- Consumo: 5.2 L/100km (un poco alto)
- Vibraciones: 0.35 g (normal)
- Velocidad media: 42 km/h
- Presión neumáticos: todas 2.25 bar (OK)
- Alerta: Revisar inyectores si sigue alto

Sábado noche - Trayecto autopista 40 km:
- Consumo: 4.5 L/100km (excelente)
- Vibraciones: 0.22 g (muy bien)
- Velocidad media: 105 km/h
- Presión neumáticos: todas 2.30 bar (OK)
- Motor funcionando perfectamente

Conclusión: El motor es eficiente en ruta,
consume más en ciudad. Revisar conducción urbana.
```

---

**¡Listo para empezar! 🚗📊**

Cualquier duda, abre un **Issue** en GitHub o revisa la documentación completa en README.md.

Última actualización: Abril 2026
Versión: 2.0 (con análisis de vibraciones)
