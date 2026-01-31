import random
import string

def generar_sku_inteligente(categoria, color, talle, variante=None):
    """
     Crea un SKU estandarizado. EJ: REM-NEG-L-059
    """

    # 1. Limpiar inputs (Mayusculas y 3 letras)
    cat_code = categoria[:3].upper()
    col_code = color [:3].upper()
    tal_code = talle.upper()

    # 2. Generar un sufijo único (o usar una variante si se provee)
    if variante:
        sufijo = str(variante).zfill(3)
    else:
        # Generar 3 caracteres al azar si no hay secuencia
        sufijo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    
    sku = f"{cat_code}-{col_code}-{tal_code}-{sufijo}"
    return sku

# --- ZONA DE CONFIGURACION ---
if __name__ == "__main__":
    print("---GENERADOR DE SKU---")
    cat = input("Escriba la Categoría (ej: Remera): ")
    col = input("Escriba el Color (ej: Negro): ")
    tal = input("Escriba el talle (ej: L): ")

    cantidad = input("¿Cuántos generar? (Enter para 1): ")
    cantidad = int(cantidad) if cantidad.isdigit() else 1

    print("\n--- TUS SKUs ---")
    for i in range(cantidad):
        # Usamos el índice 'i' para que sean secuenciales (001, 002...)
        print(generar_sku_inteligente(cat,col,tal,i+1))