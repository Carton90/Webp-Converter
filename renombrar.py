import os

# Extensiones que vamos a tocar
EXTENSIONES_VALIDAS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')

def renombrar_lote (carpeta, nombre_base, estilo):
    """
    Estilo 1 (sufijo): nombre_01.ext
    Estilo 2 (prefijo): 01_nombre.ext
    """

    # 1. Obtenemos lista de archivos y ORDENAMOS
    # Es crucial ordenar para que la secuencia tenga sentido
    archivos = sorted([f for f in os.listdir(carpeta) if f.lower().endswith(EXTENSIONES_VALIDAS)])

    total = len(archivos)
    print(f"--- Renombrando {total} archivos en '{carpeta}' ---")

    # Calculamos cuantos ceros necesitamos (si son 100 fotos, necesitamos 001, no 01)
    # zfill se encarga de rellenar con ceros
    digitos = len(str(total))
    if digitos < 2:
        digitos = 2 # Minimo siempre 2 digitos (01)

    for i, archivo in enumerate(archivos):
        # Obtener extension original (ej: .jpg)
        _, ext = os.path.splitext(archivo)

        # Crear el numero secuencial (i arranca en 0, sumamos 1)
        numero = str(i + 1).zfill(digitos)

        # Definir nuevo nombre segun estilo
        if estilo == 1:
            nuevo_nombre = f"{nombre_base}_{numero}{ext}"
        else: # Prefijo
            nuevo_nombre = f"{numero}_{nombre_base}{ext}"
        
        # Rutas completas
        ruta_vieja = os.path.join(carpeta, archivo)
        ruta_nueva = os.path.join(carpeta, nuevo_nombre)

        try:
            os.rename(ruta_vieja, ruta_nueva)
            print(f"✅ {archivo} -> {nuevo_nombre}")
        except Exception as e:
            print(f"❌ Error renombrando {archivo}: {e}")
    
    print(f"--- Renombramiento completado: {total} archivos procesados ---")

# ZONA DE PRUEBAS

if __name__ == "__main__":
    carpeta = input("Carpeta: ").strip('"')
    nombre = input("Nombre base (ej: producto-verano): ")
    print("1. Sufijo (nombre_01.ext)")
    print("2. Prefijo (01_nombre.ext)")
    opcion = input("Elige estilo (1 o 2): ")

    if os.path.isdir(carpeta) and opcion in ('1', '2'):
        renombrar_lote(carpeta, nombre, int(opcion))
    else:
        print("Carpeta no valida o opcion incorrecta.")
