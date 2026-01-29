from pathlib import Path
from PIL import Image

# Extensiones validas para procesar (Se ignoran los archivos que no tengan estas extensiones)
EXTENSIONES_VALIDAS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.ico')
FORMATOS_CON_TRANSPARENCIA = ('png', 'webp', 'ico')
FORMATOS_JPG = ('jpg', 'jpeg')

def convertir_imagen(ruta_origen, ruta_destino, formato_limpio):
    """Convierte una imagen individual al formato especificado."""
    try:
        with Image.open(ruta_origen) as img:
            # Manejar transparencia según el formato
            if formato_limpio in FORMATOS_JPG and img.mode in ('RGBA', 'LA'):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode == 'RGBA' and formato_limpio not in FORMATOS_CON_TRANSPARENCIA:
                img = img.convert('RGB')
            
            # Guardar con parámetros optimizados
            save_kwargs = {}
            if formato_limpio in FORMATOS_JPG:
                save_kwargs['quality'] = 90
            
            img.save(ruta_destino, **save_kwargs)
        return True
    except Exception as e:
        print(f"❌ Error convirtiendo {Path(ruta_origen).name}: {e}")
        return False


def procesar_carpeta(carpeta_origen, formato_salida):
    """
    Convierte todas las imágenes en una carpeta al formato especificado.
    carpeta_origen: Path de la carpeta que contiene las imágenes.
    formato_salida: Extensión deseada (ej: '.jpg', '.png', '.webp')
    """
    # Limpia el formato (remueve el punto si está presente)
    formato_limpio = formato_salida.lstrip('.').lower()
    
    # Usa pathlib para mejor manejo de rutas
    carpeta_origen = Path(carpeta_origen)
    nombre_carpeta_destino = f"Convertidas_a_{formato_limpio.upper()}"
    ruta_destino = carpeta_origen / nombre_carpeta_destino
        
    # Crea la carpeta de destino
    ruta_destino.mkdir(parents=True, exist_ok=True)
    print(f"📁 Carpeta destino: {ruta_destino}")
    
    # Filtra solo imágenes válidas (excluye la carpeta de destino)
    archivos_imagen = [
        f for f in carpeta_origen.iterdir() 
        if f.is_file() and f.suffix.lower() in EXTENSIONES_VALIDAS
    ]
    
    if not archivos_imagen:
        print("⚠️ No se encontraron imágenes para convertir.")
        return
    
    print(f"--- Iniciando conversión de {len(archivos_imagen)} archivos a formato '{formato_limpio}' ---")

    contador = 0
    # Procesa los archivos
    for archivo_origen in archivos_imagen:
        # Preparar nombres y rutas
        nombre_sin_ext = archivo_origen.stem
        nombre_archivo_salida = f"{nombre_sin_ext}.{formato_limpio}"
        ruta_completa_destino = ruta_destino / nombre_archivo_salida
        
        # Convertir imagen
        if convertir_imagen(str(archivo_origen), str(ruta_completa_destino), formato_limpio):
            contador += 1
            print(f"✅ [{contador}] Convertido: {archivo_origen.name}")
    
    print(f"\n✨ Proceso finalizado. {contador}/{len(archivos_imagen)} imágenes guardadas en: {ruta_destino}")

if __name__ == "__main__":
    carpeta = input("Arrastra la carpeta aquí o escribe la ruta: ").strip('"')
    formato = input("Escribe el formato de salida (jpg, png, webp): ").strip().lstrip('.')
    
    if Path(carpeta).is_dir():
        procesar_carpeta(carpeta, formato)
    else:
        print("❌ La ruta proporcionada no es una carpeta válida.")
