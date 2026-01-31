import os
import qrcode
from PIL import Image

def crear_qr(datos, nombre_salida, carpeta_destino="Codigos_QR"):
    # Crear la carpeta si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    try:
        # Configuración del QR (versión 1 es el mas pequeño, box_size es el tamaño de pixeles)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(datos)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Asegurar extensión
        if not nombre_salida.lower().endswith('.png'):
            nombre_salida += ".png"

        ruta_final = os.path.join(carpeta_destino, nombre_salida)
        img.save(ruta_final)
        print(f"✅ QR guardado en: {ruta_final}")
    except Exception as e:
        print(f"❌ Error al crear el QR: {e}")

if __name__ == "__main__":
    datos = input("Ingresa la URL o Texto para el QR: ")
    nombre = input("Nombre del archivo de salida (ej: producto_01): ")
    crear_qr(datos, nombre)