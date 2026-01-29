import os
from PIL import Image

# Extensiones que vamos a buscar para optimizar
EXTENSIONES_ENTRADA = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')

def optimizar_para_web(carpeta_origen, calidad=80):
    # 1. Crear carpeta de salida
    nombre_carpeta = "Optimizado_Web"
    ruta_destino = os.path.join(carpeta_origen, nombre_carpeta)

    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)
        print(f"📁 Carpeta creada: {ruta_destino}")
    
    archivos = os.listdir(carpeta_origen)

    total_ahorrado = 0
    contador = 0

    print(f"--- Optimizando imagenes a Webp (Calidad: {calidad}%) ---")

    for archivo in archivos:
        # Omitir la carpeta de destino
        if archivo == nombre_carpeta:
            continue

        if archivo.lower().endswith(EXTENSIONES_ENTRADA):
            ruta_origen = os.path.join(carpeta_origen, archivo)

            # Definir nombre de salida con extensión .webp
            nombre_sin_ext = os.path.splitext(archivo)[0]
            nombre_salida = f"{nombre_sin_ext}.webp"
            ruta_salida = os.path.join(ruta_destino,nombre_salida)

            try:
                # Obtener peso original para comparar
                peso_original = os.path.getsize(ruta_origen)
                with Image.open(ruta_origen) as img:
                    # Pillow elimina exif automáticamente al guardar una nueva imagen
                    # a menos que le pases el parametro exif explícitamente.

                    # method=6 es la compresion más lenta pero efectiva
                    img.save(ruta_salida, 'WEBP', quality=calidad, method=6)

                    # Calcular ahorro
                    peso_final = os.path.getsize(ruta_salida)
                    ahorro = peso_original - peso_final
                    total_ahorrado += ahorro

                    # Mostrar porcentaje de reduccion
                    reduccion = ((peso_original - peso_final) / peso_original) * 100
                    print(f"✅ {archivo} -> WebP | Reducción: {reduccion:.1f}%")
                    contador += 1
        
            except Exception as e:
                print(f"❌ Error optimizando {archivo}: {e}")

    # Convertir bytes a MB para el reporte final
    ahorro_mb = total_ahorrado / (1024 * 1024)
    print(f"📊 Imágenes procesadas: {contador}")
    print(f"💾 Espacio total ahorrado en disco/servidor: {ahorro_mb:.2f} MB")

# --- ZONA DE CONFIGURACIÓN ---
if __name__ == "__main__":
    carpeta = input("Arrastra la carpeta con imágenes aquí o escribe la ruta: ").strip('"')

    # Opcion de calidad
    calidad_input = input("Calidad de compresión WebP (1-100, Enter para usar default 80): ").strip()
    calidad = int (calidad_input) if calidad_input.isdigit() else 80

    if os.path.isdir(carpeta):
        optimizar_para_web(carpeta, calidad)
    else:
        print("❌ Ruta Invalida.")
            
