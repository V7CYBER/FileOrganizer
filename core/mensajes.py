def mostrar_error(nombre_archivo, motivo):

    print("\n" + "━" * 40)
    print("⚠ ERROR")
    print("━" * 40)

    print(f"\nArchivo:")
    print(f"  {nombre_archivo}")

    print(f"\nMotivo:")
    print(f"  {motivo}")

    print("\nEl programa continuará.")
    print("━" * 40)

    

def mostrar_error_ruta(ruta):

    print("\n" + "━" * 40)
    print("⚠ ERROR")
    print("━" * 40)

    print("\nLa carpeta indicada no existe.")

    print("\nRuta introducida:")
    print(f"  {ruta}")

    print("\nComprueba la ruta e inténtalo de nuevo.")
    print("━" * 40)