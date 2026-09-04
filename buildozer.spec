[app]

# Nombre que aparecerá en el celular
title = Control de Ventas

# Nombre interno de la aplicación
package.name = controlventas

# Dominio interno
package.domain = org.yancen

# Carpeta donde está main.py
source.dir = .

# Archivos que se incluirán
source.include_exts = py,png,jpg,jpeg,kv,json,txt

# Versión
version = 1.0

# Dependencias de Python
requirements = python3,kivy

# Orientación
orientation = portrait

# Pantalla completa
fullscreen = 0

# Permitir aceptar automáticamente las licencias del SDK
android.accept_sdk_license = True

# API mínima de Android
android.minapi = 23

# Arquitecturas para celulares Android
android.archs = arm64-v8a, armeabi-v7a

# Copiar los archivos JSON dentro de la aplicación
android.private_storage = True


[buildozer]

log_level = 2
warn_on_root = 1
