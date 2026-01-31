@echo off
title Herramienta de Imagenes
color 1F

:: Cambiar al directorio donde esta este archivo .bat
cd /d "%~dp0"

echo Iniciando sistema...
python launcher.py

:: Si el programa se cierra por error, que no se cierre la ventana negra inmediatamente
if %errorlevel% neq 0 (
    echo.
    echo ------------------------------------------------
    echo OCURRIO UN ERROR INESPERADO.
    echo Revisa si borraste algun archivo .py
    echo ------------------------------------------------
    pause
)