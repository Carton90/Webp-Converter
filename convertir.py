import os
from PIL import Image

def convertir_imagen(ruta_imagen, formato_salida):
    """
    Convierte una imagen al formato especificado.
    ruta_imagen: Path del archivo (ej: 'foto.webp')
    formato_salida: Extensión deseada (ej: 'jpg', 'png', 'ico')
    """
    try:
        # Abrir la imagen
        with Image.open(ruta_imagen) as img:
            nombre_base, _ = os.path.splitext(ruta_imagen)
            nombre_salida = f"{nombre_base}.{formato_salida.lower()}"
            
            # CASO ESPECIAL: Si convertimos a JPG y la imagen tiene transparencia (RGBA)
            # JPG no soporta transparencia, así que hay que convertirla a RGB con fondo blanco.
            if formato_salida.lower() in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'LA'):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1]) # Usar el canal alfa como máscara
                img = background
            
            # Si es otro formato que no soporta RGBA (opcional, dependiendo del caso)
            elif img.mode == 'RGBA' and formato_salida.lower() not in ['png', 'webp', 'ico']:
                img = img.convert('RGB')

            # Guardar
            img.save(nombre_salida, quality=90) # quality es ignorado por PNG, pero útil para JPG/WEBP
            print(f"✅ Éxito: Guardado como {nombre_salida}")

    except Exception as e:
        print(f"❌ Error convirtiendo {ruta_imagen}: {e}")

# --- ZONA DE CONFIGURACIÓN ---
if __name__ == "__main__":
    # Puedes cambiar esto para que pida input al usuario o procese una carpeta entera
    archivo = input("Arrastra la imagen aquí o escribe la ruta: ").strip('"') # .strip elimina comillas si arrastras el archivo
    formato = input("Escribe el formato de salida (jpg, png, webp): ").strip()
    
    convertir_imagen(archivo, formato)