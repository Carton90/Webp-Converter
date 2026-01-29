import os
from PIL import Image

# Extensiones validas para procesar (Se ignoran los archivos que no tengan estas extensiones)
EXTENSIONES_VALIDAS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.ico')

def procesar_carpeta(carpeta_origen, formato_salida):
    """
    Convierte todas las imágenes en una carpeta al formato especificado.
    carpeta_origen: Path de la carpeta que contiene las imágenes.
    formato_salida: Extensión deseada (ej: '.jpg', '.png', '.webp')
    """
    # Limpia el formato (remueve el punto si está presente)
    formato_limpio = formato_salida.lstrip('.').lower()
    
    # 1 Crea la carpeta de destino
    nombre_carpeta_destino = f"Convertidas_a_{formato_limpio.upper()}"
    ruta_destino = os.path.join(carpeta_origen, nombre_carpeta_destino)
        
    # Verifica si existe la carpeta en el path dado y la crea.
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)
        print(f"📁 Carpeta creada: {ruta_destino}")
        
    archivos = os.listdir(carpeta_origen)
    contador = 0

    print(f"--- Iniciando conversion de {len(archivos)} archivos en '{carpeta_origen}' a formato '{formato_limpio}' ---")

    # 2 Recorre los archivos
    for archivo in archivos:
        # Omitir la carpeta de destino
        if archivo == nombre_carpeta_destino:
            continue
        # Filtra solo imagenes
        if archivo.lower().endswith(EXTENSIONES_VALIDAS):
            ruta_completa_origen = os.path.join(carpeta_origen, archivo)

            try:
                with Image.open(ruta_completa_origen) as img:
                    # Preparar nombre de salida
                    nombre_sin_ext = os.path.splitext(archivo)[0]
                    nombre_archivo_salida = f"{nombre_sin_ext}.{formato_limpio}"
                    ruta_completa_destino = os.path.join(ruta_destino, nombre_archivo_salida)

                    # CASO ESPECIAL: Si convertimos a JPG y la imagen tiene transparencia (RGBA)
                    # JPG no soporta transparencia, así que hay que convertirla a RGB con fondo blanco

                    if formato_limpio in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'LA'):
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    elif img.mode == 'RGBA' and formato_limpio not in ['png', 'webp', 'ico']:
                        img = img.convert('RGB')

                    # Guardar la imagen convertida
                    img.save(ruta_completa_destino, quality=90)
                    contador += 1
                    print(f"✅ [{contador}] Convertido: {archivo}")
            except Exception as e:
                print(f"❌ Error convirtiendo {archivo}: {e}")
    print(f"\n✨ Proceso finalizado. {contador} imágenes guardadas en: {ruta_destino}")
if __name__ == "__main__":
    carpeta = input("Arrastra la carpeta aquí o escribe la ruta: ").strip('"')
    formato = input("Escribe el formato de salida (jpg, png, webp): ").strip().lstrip('.')

    if os.path.isdir(carpeta):
        procesar_carpeta(carpeta, formato)
    else:
        print("❌ La ruta proporcionada no es una carpeta válida.") 
