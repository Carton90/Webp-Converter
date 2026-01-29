import os
from PIL import Image

EXTENSIONES_VALIDAS = ('jpg', 'jpeg', 'png', 'webp')

def aplicar_marca_agua(carpeta_origen, ruta_logo, escala_pct=15, opacidad=0.8):
    """
    Superpone un logo en la esquina inferior derecha.
    escala_pct: Qué porcentaje del ancho de la foto ocupará el logo (ej: 15%).
    opacidad: Opacidad del logo (1.0 = completamente opaco, 0.0 = invisible)
    """
    # 1. Crear la carpeta de salida
    nombre_carpeta = "Con_Marca_de_Agua"
    ruta_destino = os.path.join(carpeta_origen, nombre_carpeta)

    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)
    
    # 2. Cargar el logo
    try:
        # Cargar el logo una sola vez para no abrirlo en cada iteración
        logo_original = Image.open(ruta_logo).convert("RGBA")
    except Exception as e:
        print(f"❌ Error cargando el logo: {e}")
        return

    archivos = os.listdir(carpeta_origen)
    contador = 0

    print(f"--- Aplicando marca de agua (Escala: {escala_pct}%), Opacidad: {opacidad*100}%)  ---")

    for archivo in archivos:
        if archivo.lower().endswith(EXTENSIONES_VALIDAS):
            ruta_imagen = os.path.join(carpeta_origen, archivo)
            ruta_salida = os.path.join(ruta_destino, archivo)
            try:
                with Image.open(ruta_imagen) as img:
                    # Convertir a RGBA para manejar transparencias
                    # Si era JPG, esto es necesario para pegar el PNG encima sin lios
                    img_base = img.convert("RGBA")
                    ancho_base, alto_base = img_base.size

                    # Calcular nuevo tamaño del logo
                    # Queremos que el logo sea el X% del ancho de la imagen
                    margen = int(ancho_base * 0.05)  # 5% de margen
                    ancho_logo_objetivo = int((escala_pct / 100) * ancho_base)

                    # Asegurar que el logo no sea más ancho que el espacio disponible
                    max_ancho_logo = max(1, ancho_base - 2 * margen)
                    if ancho_logo_objetivo > max_ancho_logo:
                        ancho_logo_objetivo = max_ancho_logo

                    # Calcular el alto proporcional
                    ratio_logo = logo_original.height / logo_original.width
                    alto_logo_objetivo = max(1, int(ancho_logo_objetivo * ratio_logo))

                    # Redimensionar el logo (usando copia)
                    logo_redimensionado = logo_original.resize((ancho_logo_objetivo, alto_logo_objetivo), Image.Resampling.LANCZOS)

                    # Calcular posicion (Esquina inferior derecha), evitando coordenadas negativas
                    pos_x = max(margen, ancho_base - ancho_logo_objetivo - margen)
                    pos_y = max(margen, alto_base - alto_logo_objetivo - margen)

                    # Aplicar opacidad solo a las partes NO transparentes
                    if 0 < opacidad < 1:
                        # Separar los canales RGBA
                        r, g, b, a = logo_redimensionado.split()
                        # Multiplicar el canal alfa por la opacidad deseada
                        # Esto mantiene las áreas transparentes transparentes
                        a = a.point(lambda p: int(p * opacidad))
                        # Recombinar los canales
                        logo_redimensionado = Image.merge('RGBA', (r, g, b, a))
                    
                    # Pegar el logo directamente sobre la imagen base
                    # El tercer parámetro (logo_redimensionado) actúa como máscara de transparencia
                    img_base.paste(logo_redimensionado, (pos_x, pos_y), logo_redimensionado)

                    # Guardar la imagen
                    if archivo.lower().endswith(('jpg', 'jpeg')):
                        img_final = img_base.convert("RGB")
                        img_final.save(ruta_salida, quality=95)
                    else:
                        img_base.save(ruta_salida)
                    
                    contador += 1
                    print(f"✅ Marca aplicada a: {archivo}")
            except Exception as e:
                print(f"❌ Error procesando {archivo}: {e}")
    print(f"\n✨ Proceso terminado. Imágenes guardadas en: {ruta_destino}")

# ZONA DE CONFIGURACIÓN ---
if __name__ == "__main__":
    carpeta = input("Arrastra la carpeta de fotos: ").strip('"')
    logo = input("Arrastra el archivo del logo (PNG): ").strip('"')
    escala = input("Escala del logo en % (por defecto 15): ").strip()
    opacidad_input = input("Opacidad del logo 0-100 (por defecto 80): ").strip()

    if os.path.isdir(carpeta) and os.path.isfile(logo):
        try:
            escala = int(escala) if escala else 15
            opacidad_pct = int(opacidad_input) if opacidad_input else 80
            opacidad = opacidad_pct / 100.0
            aplicar_marca_agua(carpeta, logo, escala_pct=escala, opacidad=opacidad)
        except ValueError:
            print("❌ La escala debe ser un número entero.")
    else:
        print("❌ Verifica que las rutas de la carpeta y del logo sean correctas.")
                    