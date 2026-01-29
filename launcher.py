import os
import sys

# Importamos tus otros scripts como si fueran librerías
# Asegurate de que los archivos .py esten en la misma carpeta

try:
    import convertir_lote
    import redimensionar
    import optimizar_web as optimizar
    import marca_agua
    import renombrar
except ImportError as e:
    print(f"❌ Error: Faltan scripts en la carpeta.")
    print(f"Detalles: {e}")
    sys.exit()

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    limpiar_consola()
    print("======================================")
    print("   🛠️  CENTRO DE COMANDO DE IMÁGENES   ")
    print("========================================")
    print("1. 🔄 Convertir Formatos (ej: PNG -> JPG)")
    print("2. 📏 Redimensionar Lote (ej: a 1080px)")
    print("3. 🚀 Optimizar para Web (WebP + Compresión)")
    print("4. ©  Aplicar Marca de Agua")
    print("5. 🏷️  Renombrar Secuencialmente")
    print("----------------------------------------")
    print("0. Salir")
    print("========================================")

def main():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (0-5): ")

        if opcion == '0':
            print("👋 Saliendo... ¡Hasta luego!")
            break

        # --- LOGICA DE LLAMADAS ---

        # CASO 1: CONVERTIR LOTE
        elif opcion == '1':
             print("\n--- MÓDULO DE CONVERSIÓN ---")
             carpeta = input("📁 Arrastra la carpeta origen: ").strip('"')
             formato = input("🔤 Formato destino (ej: jpg, png, webp): ").strip()

             # Llamamos a la función del archivo convertir_lote.py
             if os.path.isdir(carpeta):
                convertir_lote.procesar_carpeta(carpeta, formato)
             else:
                print("❌ La ruta proporcionada no es una carpeta válida.")
             input("\nPresiona Enter para volver al menú...")
        
        # CASO 2: REDIMENSIONAR
        elif opcion == '2':
            print("\n--- MÓDULO DE REDIMENSIÓN ---")
            carpeta = input("📁 Arrastra la carpeta origen: ").strip('"')
            try:
                ancho = int(input("📐 Ancho deseado en píxeles (ej: 1080): "))
                if os.path.isdir(carpeta):
                    redimensionar.redimensionar_lote(carpeta, ancho)
                else:
                    print("❌ Carpeta inválida.")
            except ValueError:
                print("❌ El ancho tiene que ser un numero")
            input("\nPresiona Enter para volver al menú...")
        
        # CASO 3: OPTIMIZAR PARA WEB
        elif opcion == '3':
            print("\n--- MÓDULO DE OPTIMIZACIÓN WEB ---")
            carpeta = input("📁 Arrastra la carpeta origen: ").strip('"')
            calidad_str = input("⚙️ Calidad deseada (1-100, por defecto 80): ").strip()
            calidad = int(calidad_str) if calidad_str.isdigit() else 80

            if os.path.isdir(carpeta):
                optimizar.optimizar_para_web(carpeta, calidad)
            else:
                print("❌ Carpeta inválida.")
            input("\nPresiona Enter para volver al menú...")

        # CASO 4: MARCA DE AGUA
        elif opcion == '4':
            print("\n--- MÓDULO MARCA DE AGUA ---")
            carpeta = input("📁 Arrastra la carpeta origen: ").strip('"')
            logo = input(" Arrastra el archivo del LOGO: ").strip('"')

            if os.path.isdir(carpeta) and os.path.isfile(logo):
                marca_agua.aplicar_marca_agua(carpeta, logo)
            else:
                print("❌ Rutas inválidas")
            input("\nPresiona Enter para volver al menú...")

        # CASO 5: RENOMBRAR
        elif opcion == '5':
            print("\n--- MÓDULO DE RENOMBRADO ---")
            carpeta = input("📁 Arrastra la carpeta origen: ").strip('"')
            nombre_base = input("Nombre base para los archivos (sin espacios preferiblemente): ").strip()

            print("¿Dónde quieres el número?")
            print("1. Final (camisa_01.jpg) - Recomendado")
            print("2. Principio (01_camisa.jpg)")
            estilo = input("Selecciona 1 o 2: ").strip()

            if os.path.isdir(carpeta):
                renombrar.renombrar_lote(carpeta, nombre_base, estilo)
            else:
                print("❌ Carpeta inválida.")
            input("\nPresiona Enter para volver al menú...")

        else:
            print("❌ Opción no válida.")
            input("Enter para continuar...")

if __name__ == "__main__":
    main()