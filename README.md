# CrackingTheOCCMundial
Cracking the code to automate OCC Mundial applications. Built with Python and Playwright.

# Playwright + Python - Automatización de postulación a empleos

## 📋 Requisitos
- Python 3.8+
- pip

## 🚀 Instalación rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

# 2. Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Instalar navegadores de Playwright
playwright install
```
## ⚙️ Configuración

Antes de ejecutar, asegúrate de crear el siguiente archivo, siguiendo el ejemplo del archivo '.env.example' pero el
nuevo archivo debe llevar el nombre '.env', estructura va como:
```bash
# Tus credenciales de OCC Mundial
EMAIL_0=tu_correo@ejemplo.com
EMAIL_1=tu_correo+occmundial1@ejemplo.com
EMAIL_2=...
.
.
.
EMAIL_n=...

PASSWORD='your_password'

# URL
URL_OCC=https://www.occ.com.mx/
```
preferible usar gmail.com, porque occ mundia te permite crear varias cuentas asociadas al mismo correo, por ejemplo
si tu correco es tu_correo@gmail.com, puedes crear otro correo que sea tu_correo+occ1@gmail.com y aun asi
los correos enviados a este nuevo correo seran direccionados al correo original, es decir puedes crear
multiples cuentas asociadas al mismo correo, funciona para N correos, automaticamente cierra sesion y abre la nueva.

## 🏃‍♂️ Ejecutar el bot
```bash
python main.py
```

