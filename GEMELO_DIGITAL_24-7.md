# 🚀 GEMELO DIGITAL 24/7 EN GITHUB

## ¿QUÉ ES ESTO?

Sistema automático que genera gráficos 3D del gemelo digital cada vez que:
- ✅ Subes datos Excel a GitHub
- ✅ Se ejecuta cada hora automáticamente (opcional)
- ✅ Se publica en GitHub Pages
- ✅ Accesible desde cualquier navegador 24/7

---

## 📋 REQUISITOS

1. **Cuenta GitHub** (gratuita)
2. **Git instalado** en tu PC
3. **Python 3.8+** instalado
4. **Los 8 archivos del proyecto**

---

## 🎯 ESTRUCTURA FINAL EN GITHUB

```
obd2-dashboard-skoda/
├── .github/
│   └── workflows/
│       └── gemelo-digital.yml          ← GitHub Actions
├── obd2-app.html                       ← PWA iOS
├── analisis_obd2.py                    ← Análisis
├── gemelo_digital.py                   ← Gemelo 3D
├── requirements.txt                    ← Dependencias
├── README.md                           ← Documentación
├── GITHUB_SETUP.md                     ← Guía GitHub
├── QUICK_START.md                      ← Quick start
├── .gitignore                          ← Ignorar archivos
├── data/                               ← Carpeta datos
│   ├── sample-obd2.xlsx                ← Ejemplo Excel
│   └── .gitkeep
├── output/                             ← Gráficos generados
│   └── .gitkeep
└── docs/                               ← GitHub Pages
    ├── index.html                      ← Página principal
    └── .gitkeep
```

---

## 🔄 GITHUB ACTIONS WORKFLOW

### ¿QUÉ HACE?

El archivo `.github/workflows/gemelo-digital.yml` automáticamente:

1. **Detecta cambios** en archivos Excel en carpeta `data/`
2. **Ejecuta Python** con `gemelo_digital.py`
3. **Genera gráficos** 3D HTML
4. **Publica en GitHub Pages** (página web pública)
5. **Envía notificación** con link a los gráficos

### DIAGRAMA:

```
Subes archivo.xlsx a GitHub
              ↓
GitHub Actions detecta cambio
              ↓
Ejecuta: python gemelo_digital.py
              ↓
Genera 8 gráficos 3D
              ↓
Publica en GitHub Pages
              ↓
Link accesible 24/7:
https://tu-usuario.github.io/obd2-dashboard-skoda/
```

---

## 📥 PASO 1: CREAR REPOSITORIO GITHUB

### 1. Ir a GitHub
```
https://github.com/new
```

### 2. Crear repositorio
```
Nombre: obd2-dashboard-skoda
Descripción: Gemelo Digital Škoda Octavia 1.5 TSI 2024
Público: ✅ SI
```

### 3. Click "Create repository"

---

## 🖥️ PASO 2: PREPARAR CARPETA LOCAL

```bash
# Crear carpeta
mkdir obd2-dashboard-skoda
cd obd2-dashboard-skoda

# Copiar TODOS estos archivos aquí:
# - obd2-app.html
# - analisis_obd2.py
# - gemelo_digital.py
# - requirements.txt
# - README.md
# - GITHUB_SETUP.md
# - QUICK_START.md
# - .gitignore

# Crear carpetas necesarias
mkdir -p .github/workflows
mkdir -p data
mkdir -p output
mkdir -p docs

# Crear archivo GitHub Actions (ver paso 3)
```

---

## ⚙️ PASO 3: CREAR GITHUB ACTIONS WORKFLOW

### Crear archivo: `.github/workflows/gemelo-digital.yml`

```yaml
name: Generar Gemelo Digital 🚗

on:
  push:
    paths:
      - 'data/*.xlsx'
  schedule:
    - cron: '0 * * * *'  # Cada hora
  workflow_dispatch:  # Manual

jobs:
  gemelo-digital:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configurar Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Instalar dependencias
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Buscar archivo Excel más reciente
      id: find_excel
      run: |
        LATEST_XLSX=$(find data -name "*.xlsx" -type f -printf '%T@ %p\n' | sort -rn | head -1 | cut -d' ' -f2-)
        if [ -z "$LATEST_XLSX" ]; then
          echo "No hay archivos Excel en data/"
          exit 1
        fi
        echo "ARCHIVO_XLSX=$LATEST_XLSX" >> $GITHUB_OUTPUT
        echo "Procesando: $LATEST_XLSX"
    
    - name: Generar Gemelo Digital
      run: |
        python gemelo_digital.py "${{ steps.find_excel.outputs.ARCHIVO_XLSX }}"
    
    - name: Mover gráficos a docs/
      run: |
        mkdir -p docs
        mv gemelo_digital_*.html docs/ 2>/dev/null || true
        
        # Crear index.html si no existe
        if [ ! -f docs/index.html ]; then
          cp gemelo_digital_indice.html docs/index.html 2>/dev/null || true
        else
          cp gemelo_digital_indice.html docs/index.html
        fi
    
    - name: Configurar Git
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Actions"
    
    - name: Commit cambios
      run: |
        git add -A
        git diff-index --quiet HEAD || git commit -m "🚗 Gemelo Digital actualizado automáticamente"
    
    - name: Push cambios
      uses: ad-m/github-push-action@master
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        branch: ${{ github.ref }}
    
    - name: Crear comentario en commit
      if: always()
      uses: actions/github-script@v6
      with:
        script: |
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: '✅ Gemelo Digital generado!\n\n👉 Ver en: https://${{ github.repository_owner }}.github.io/${{ github.event.repository.name }}/'
          })
```

---

## 📤 PASO 4: SUBIR A GITHUB

```bash
# En la carpeta del proyecto

# 1. Inicializar Git
git init

# 2. Agregar todos los archivos
git add .

# 3. Crear primer commit
git commit -m "Inicial: Gemelo Digital Škoda Octavia 24/7 en GitHub"

# 4. Cambiar rama a main
git branch -M main

# 5. Agregar repositorio remoto
git remote add origin https://github.com/TU_USUARIO/obd2-dashboard-skoda.git

# 6. Subir código
git push -u origin main

# Cuando pida contraseña: usar token de GitHub
# (Settings → Developer settings → Personal access tokens → Generate new token)
```

---

## 🌐 PASO 5: ACTIVAR GITHUB PAGES

### En GitHub:

1. Ir a: **Settings** → **Pages**
2. **Source:** seleccionar `main` (o `master`)
3. **Folder:** seleccionar `/docs`
4. Click **Save**

### Esperar 1-2 minutos

Tu página estará en:
```
https://tu-usuario.github.io/obd2-dashboard-skoda/
```

---

## 📊 PASO 6: SUBIR DATOS EXCEL

### Opción A: Desde Windows (Recomendado)

```bash
# 1. Copiar tu Excel a la carpeta data/
cp "C:\Descargas\obd2-consumo-2026-04-06.xlsx" data/

# 2. Commit y push
git add data/
git commit -m "Agregar datos OBD2 del 06/04/2026"
git push

# 3. GitHub Actions se ejecuta automáticamente
# 4. Ver gráficos en: https://tu-usuario.github.io/obd2-dashboard-skoda/
```

### Opción B: Desde GitHub Web

```
1. Ir a tu repositorio en GitHub
2. Carpeta: data/
3. Upload files
4. Seleccionar Excel
5. Commit changes
6. GitHub Actions se ejecuta automáticamente
```

### Opción C: Automático cada hora

El workflow se ejecuta cada hora automáticamente
(puedes cambiar en `.github/workflows/gemelo-digital.yml`)

---

## 🔗 PASO 7: ACCEDER A GRÁFICOS

### URL PÚBLICA:
```
https://tu-usuario.github.io/obd2-dashboard-skoda/
```

### CONTENIDO:
- 📊 Tablero Principal
- 🏎️ Motor 3D
- 🔥 Mapa de Calor
- 📳 Vibraciones 3D
- 🏁 Dinámica Conducción
- 🔗 Correlaciones 3D
- 🔍 Diagnóstico
- 🚗 Vehículo 3D

**TODOS INTERACTIVOS Y EN VIVO**

---

## 📱 CREAR ARCHIVO DE EJEMPLO

Para que funcione antes de subir datos:

### Crear: `data/sample-obd2.xlsx`

```python
# En Windows, ejecutar una vez:
python -c "
import pandas as pd
import numpy as np

# Crear datos de ejemplo
n = 1000
df = pd.DataFrame({
    'timestamp': pd.date_range('2026-04-06', periods=n, freq='100ms'),
    'rpm': np.random.normal(3000, 1000, n),
    'speed': np.random.normal(60, 20, n),
    'consumoInstantaneo': np.random.normal(5.0, 1.0, n),
    'power': np.random.normal(80, 30, n),
    'coolantTemp': np.random.normal(90, 10, n),
    'acelerometerX': np.random.normal(0.1, 0.2, n),
    'acelerometerY': np.random.normal(0.1, 0.2, n),
    'acelerometerZ': np.random.normal(0.2, 0.3, n),
    'vibracionMagnitud': np.abs(np.random.normal(0.3, 0.2, n)),
    'tirePressureLF': np.random.normal(2.25, 0.1, n),
    'tirePressureRF': np.random.normal(2.25, 0.1, n),
    'tirePressureLR': np.random.normal(2.25, 0.1, n),
    'tirePressureRR': np.random.normal(2.25, 0.1, n),
})

# Guardar Excel
df.to_excel('data/sample-obd2.xlsx', sheet_name='OBD2 Data', index=False)
print('✅ Archivo de ejemplo creado: data/sample-obd2.xlsx')
"
```

Luego:
```bash
git add data/sample-obd2.xlsx
git commit -m "Agregar archivo de ejemplo para demostración"
git push
```

---

## 🎯 FLUJO COMPLETO

```
┌─────────────────────────────────────┐
│ 1. Grabar datos en iPhone (PWA)    │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│ 2. Descargar Excel desde app       │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│ 3. Subir Excel a data/ en GitHub   │
│    (Web o Git push)                │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│ 4. GitHub Actions detecta cambio   │
│    y se ejecuta automáticamente    │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│ 5. Python ejecuta gemelo_digital.py│
│    Genera 8 gráficos 3D            │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│ 6. Publica en GitHub Pages         │
│    URL pública 24/7 disponible     │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│ 7. Acceso desde navegador:         │
│ https://tu-user.github.io/repo/    │
│                                     │
│ ✅ Gemelo Digital VIVO 24/7        │
└─────────────────────────────────────┘
```

---

## 🔍 MONITOREAR EJECUCIONES

### Ver estado de GitHub Actions:

1. Ir a tu repositorio en GitHub
2. **Actions** (pestaña superior)
3. Ver ejecuciones y logs
4. Si hay error, leerlo en **Logs**

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### "GitHub Actions no se ejecuta"

1. Verificar que el archivo Excel está en `data/`
2. Verificar que `.github/workflows/gemelo-digital.yml` existe
3. Ir a **Settings** → **Actions** → activar "Read and write permissions"

### "Página GitHub Pages no aparece"

1. **Settings** → **Pages**
2. Source: `main` branch, `/docs` folder
3. Esperar 2-3 minutos

### "Error en Python"

1. Ir a **Actions**
2. Click en ejecución fallida
3. Abrir logs
4. Ver error específico
5. Actualizar `requirements.txt` si es necesario

---

## 📈 ESTADÍSTICAS EN VIVO

GitHub mostrará automáticamente:

```
✅ Ejecuciones totales
✅ Ejecuciones exitosas
✅ Ejecuciones fallidas
✅ Tiempo promedio
✅ Histórico de cambios
```

---

## 🎨 PERSONALIZAR

### Cambiar frecuencia de ejecución:

En `.github/workflows/gemelo-digital.yml`:

```yaml
schedule:
  - cron: '0 * * * *'  # Cada hora
  # Cambiar a:
  # - cron: '0 */6 * * *'  # Cada 6 horas
  # - cron: '0 0 * * *'    # Una vez al día
  # - cron: '0 0 * * 0'    # Una vez a la semana
```

### Cambiar nombre de repositorio:

Cambiar TODAS las referencias a `obd2-dashboard-skoda`
por tu nuevo nombre

### Agregar más archivos a gitignore:

Editar `.gitignore`

---

## 🚀 CASOS DE USO

### 1. Análisis en tiempo real
```
Grabar datos → Subir Excel → Ver gráficos automáticamente
```

### 2. Comparar trayectos
```
Varios Excel en data/ → Gemelo Digital genera histórico
```

### 3. Seguimiento mantenimiento
```
Gráficos 3D muestran degradación con el tiempo
```

### 4. Compartir con mecánico
```
Link GitHub Pages compartible
Mecánico ve gráficos sin instalar nada
```

---

## 📋 ARCHIVOS NECESARIOS EN ZIP

```
✅ obd2-app.html
✅ analisis_obd2.py
✅ gemelo_digital.py
✅ requirements.txt
✅ README.md
✅ GITHUB_SETUP.md
✅ QUICK_START.md
✅ .gitignore
✅ .github/workflows/gemelo-digital.yml  ← IMPORTANTE
✅ data/.gitkeep
✅ docs/.gitkeep
✅ GEMELO_DIGITAL_24-7.md (este archivo)
```

---

## ✅ CHECKLIST FINAL

- [ ] Repositorio GitHub creado
- [ ] Carpeta local preparada
- [ ] Archivos copiados
- [ ] `.github/workflows/gemelo-digital.yml` creado
- [ ] `git init` ejecutado
- [ ] Código subido a GitHub
- [ ] GitHub Pages activado
- [ ] Archivo Excel agregado a data/
- [ ] GitHub Actions ejecutado exitosamente
- [ ] URL de GitHub Pages funciona
- [ ] Gráficos 3D visibles

---

## 📞 SOPORTE

Si algo no funciona:

1. Leer archivos incluidos en ZIP
2. Revisar logs en GitHub Actions
3. Verificar que Python 3.9+ está instalado
4. Verificar que requirements.txt está actualizado

---

## 🎉 ¡LISTO!

Ahora tienes un **GEMELO DIGITAL 24/7** funcionando en GitHub:

- ✅ Automático
- ✅ Gratis (GitHub Pages)
- ✅ Sin mantención
- ✅ Accesible desde cualquier navegador
- ✅ Compartible con cualquiera
- ✅ Histórico de cambios
- ✅ Gráficos 3D interactivos

**Cada vez que subas un Excel, los gráficos se actualizan automáticamente**

---

Versión: 2.0
Fecha: Abril 2026
Soporte: Incluido en ZIP
