import os
from PIL import Image

EXTENSIONES_VALIDAS = ('.jpg', '.jpeg', '.png', '.webp', '.ico', '.bmp', '.tiff')

def redimensionar_lote(carpeta_origen, ancho_deseado):
    """
    Redimensiona todas las imágenes en una carpeta al ancho especificado,
    manteniendo la proporción original. 
    Las imágenes redimensionadas se guardan en una subcarpeta llamada 'Redimensionadas_<ancho>px'.
    """

    # 1. Crear carpeta de salida
    nombre_carpeta= f"Redimensionadas_{ancho_deseado}px"
    ruta_destino = os.path.join(carpeta_origen, nombre_carpeta)

    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)
        print(f"✅ Carpeta creada: {ruta_destino}")

    archivos = os.listdir(carpeta_origen)
    imagenes_procesadas = 0

    print(f"--- Ajustando imágenes a {ancho_deseado}px de ancho ---")

    for archivo in archivos:
        if archivo.lower().endswith(EXTENSIONES_VALIDAS):
            ruta_origen = os.path.join(carpeta_origen, archivo)
            ruta_salida = os.path.join(ruta_destino, archivo)
            try:
                with Image.open(ruta_origen) as img:
                    # Calcular la proporción para mantener el Aspect Ratio
                    ancho_original, alto_original = img.size

                    # Si la imagen ya es más chica que el objetivo, la ignoramos o la dejamos igual
                    # Para evitar pixelearla al estirarla.
                    if ancho_original <= ancho_deseado:
                        print(f"⚠️ Saltando {archivo}: Ya es más pequeña que {ancho_deseado}px")
                        continue

                    ratio = ancho_deseado / float(ancho_original)
                    nuevo_alto = int((float(alto_original) * float(ratio)))

                    # Redimensionar usando filtro de alta calidad (LANCZOS)
                    img_redimensionada = img.resize((ancho_deseado, nuevo_alto), Image.Resampling.LANCZOS)

                    # Guardar (manteniendo el formato original)
                    img_redimensionada.save(ruta_salida, quality=95)
                    imagenes_procesadas += 1
                    print(f"✅ [{imagenes_procesadas}] {archivo}: {ancho_original}x{alto_original} -> {ancho_deseado}x{nuevo_alto}")

            except Exception as e:
                print(f"❌ Error procesando {archivo}: {e}")

    print(f"\n✨ Proceso terminado. Imágenes guardadas en: {ruta_destino}")

# --- ZONA DE CONFIGURACIÓN ---

if __name__ == "__main__":
    carpeta = input("Arrastra la carpeta aqui o escribe la ruta: ").strip('"')

    try:
        ancho = int(input("Ingresa el ancho deseado en píxeles (ej: 1080): "))
        if os.path.isdir(carpeta):
            redimensionar_lote(carpeta, ancho)
        else:
            print("❌ La ruta proporcionada no es una carpeta válida.")
    except ValueError:
        print("❌ Por favor, ingresa un número válido para el ancho.")
        