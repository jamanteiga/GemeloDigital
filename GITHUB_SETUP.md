# 📤 Guía completa: Subir a GitHub

## Paso 1: Crear cuenta GitHub (si no la tienes)

1. Ir a https://github.com
2. Click "Sign up"
3. Seguir los pasos
4. Verificar email

## Paso 2: Crear nuevo repositorio

1. En GitHub, click en **"+"** (arriba a la derecha)
2. **"New repository"**
3. **Nombre:** `obd2-dashboard-skoda`
4. **Descripción:** "Dashboard PWA para OBD2 Škoda Octavia 1.5 TSI 2024 con análisis de vibraciones"
5. **Público** (para que todos lo vean)
6. **NO marques** "Initialize with README" (lo haremos nosotros)
7. Click **"Create repository"**

## Paso 3: Configurar Git en Windows

### Instalar Git:

1. Descargar: https://git-scm.com/download/win
2. Instalar (opciones por defecto está bien)
3. Abrir CMD y verificar:
```bash
git --version
```

### Configurar identidad:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

## Paso 4: Preparar carpeta local

```bash
# Crear carpeta en tu equipo
mkdir obd2-dashboard-skoda
cd obd2-dashboard-skoda

# Copiar estos ficheros a la carpeta:
# - obd2-app.html
# - analisis_obd2.py
# - requirements.txt
# - README.md
# - .gitignore (ver abajo)
```

## Paso 5: Crear archivo .gitignore

En la carpeta `obd2-dashboard-skoda`, crear archivo `.gitignore` con contenido:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Datos
*.xlsx
*.csv
data/
*.json

# OS
.DS_Store
Thumbs.db

# Gráficos generados
*.html
!obd2-app.html
```

## Paso 6: Inicializar repositorio local

```bash
cd obd2-dashboard-skoda

# Inicializar Git
git init

# Agregar todos los archivos
git add .

# Crear primer commit
git commit -m "Inicial: OBD2 Dashboard Škoda Octavia 1.5 TSI 2024

- PWA para captura OBD2 en tiempo real
- Análisis de vibraciones con acelerómetro iPhone
- Gráficos dinámicos y estadísticas
- Script Python para análisis avanzado"

# Cambiar rama a main (estándar en GitHub)
git branch -M main
```

## Paso 7: Conectar con repositorio remoto en GitHub

```bash
# Agregar repositorio remoto
# (reemplazar TU_USUARIO con tu username de GitHub)
git remote add origin https://github.com/TU_USUARIO/obd2-dashboard-skoda.git

# Subir código
git push -u origin main
```

**En este punto te pedirá autenticación:**

### Opción A: Token de acceso (recomendado)

1. En GitHub: Configuración → Developer settings → Personal access tokens
2. Click "Generate new token"
3. Nombre: "obd2-dashboard"
4. Permisos: Marcar "repo" (acceso a repositorios)
5. Generar y copiar token
6. Pegar el token cuando te lo pida en CMD

### Opción B: Usuario y contraseña

(Menos seguro, GitHub ya no lo recomienda)

```
Usuario: tu-username-github
Contraseña: tu-contraseña
```

## Paso 8: Verificar en GitHub

Ir a https://github.com/TU_USUARIO/obd2-dashboard-skoda

Deberías ver:
- ✅ Archivos subidos (obd2-app.html, analisis_obd2.py, etc)
- ✅ README.md visible en la página principal
- ✅ Contador de "Stars" en la esquina superior derecha

## 🔄 Futuros cambios

Cada vez que modifiques archivos:

```bash
# Ver qué cambió
git status

# Agregar cambios
git add .

# Crear commit
git commit -m "Descripción del cambio"

# Subir a GitHub
git push
```

## 📋 Ejemplo completo (paso a paso)

```bash
# 1. Abrir CMD
# 2. Ir a carpeta del proyecto
cd C:\Users\TuUsuario\Documents\obd2-dashboard-skoda

# 3. Ver estado
git status

# 4. Agregar cambio
git add obd2-app.html

# 5. Describir cambio
git commit -m "Mejorar interfaz de vibraciones"

# 6. Subir
git push
```

## 🎯 Estructura final en GitHub

```
obd2-dashboard-skoda/
├── obd2-app.html              ✅ PWA principal
├── analisis_obd2.py           ✅ Script análisis
├── requirements.txt           ✅ Dependencias
├── README.md                  ✅ Documentación
├── .gitignore                 ✅ Archivos a ignorar
└── LICENSE                    (opcional: MIT License)
```

## 📊 Badges para README (opcional)

Puedes agregar estos a tu README.md:

```markdown
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
```

## 🔒 Proteger repositorio (opcional)

1. En GitHub → Settings → Branches
2. "Add rule" para rama "main"
3. Marcar:
   - "Require pull request reviews"
   - "Require status checks to pass"
   - "Dismiss stale pull request approvals"

Esto previene cambios accidentales.

## 🌟 Hacer proyecto visible

Para que más gente lo encuentre:

1. Agregar **topics** en Settings → About:
   - obd2
   - skoda
   - automotive
   - python
   - pwa
   - iot

2. Hacer **README.md bonito** con:
   - Descripción clara
   - Pantallazos (si puedes)
   - Instrucciones de uso
   - Ejemplos de código

3. Agregar **LICENSE** (MIT):
```bash
# En la carpeta, crear archivo LICENSE con:
# Copiar contenido de: https://opensource.org/licenses/MIT
```

## 🚀 Siguientes pasos

1. **Invitar colaboradores** (opcional):
   - Settings → Collaborators → Add people

2. **Crear issues** para funcionalidades futuras:
   - Issues → New Issue

3. **Crear releases** cuando hayas versiones importantes:
   - Releases → Create a new release

4. **Documentar en Wiki** (opcional):
   - Wiki → Create the first page

## 📱 Compartir proyecto

Una vez subido, puedes compartir:

```
GitHub: https://github.com/TU_USUARIO/obd2-dashboard-skoda
```

O si lo haces **público**, la gente puede:
- ⭐ Darle stars
- 🍴 Hacerle fork (copiar para sus proyectos)
- 👁️ Vigilarlo para novedades
- 💬 Abrir issues con dudas

## ✅ Checklist final

- [ ] Cuenta GitHub creada
- [ ] Repositorio creado en GitHub
- [ ] Git instalado en Windows
- [ ] Carpeta local creada
- [ ] Archivos copiados a carpeta
- [ ] `.gitignore` creado
- [ ] `git init` ejecutado
- [ ] Primer commit hecho
- [ ] `git remote add` ejecutado
- [ ] `git push` completado
- [ ] Repositorio visible en GitHub
- [ ] README.md se ve bien
- [ ] Proyecto compartido

---

**¡Listo! Tu proyecto está en GitHub y visible para el mundo! 🎉**

Cualquier duda, abre un **Issue** en GitHub o escribe un **Discussion**.
