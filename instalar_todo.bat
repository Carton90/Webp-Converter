@echo off
title Instalador de Dependencias
color 0A

echo ==========================================
echo    CONFIGURANDO ENTORNO DE IMAGENES
echo ==========================================
echo.
echo Verificando si Python esta instalado...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [ERROR] Python no esta instalado o no se agrego al PATH.
    echo Por favor instala Python desde python.org y marca la casilla "Add to PATH".
    echo.
    pause
    exit
)

echo.
echo Python detectado. Instalando librerias necesarias...
echo 1. Instalando Pillow (Imagenes)...
pip install Pillow
echo.
echo 2. Instalando Qrcode (Codigos QR)...
pip install "qrcode[pil]"

echo.
echo ==========================================
echo    LISTO! YA PUEDES USAR LA HERRAMIENTA
echo ==========================================
echo.
pause