from src.crud.usuario_crud import UsuarioCrud


def main():
    usuario_crud = UsuarioCrud()

    while True:
        print("\n--- BIBLIOTECA ---")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            documento = input("Documento: ")
            correo = input("Correo: ")
            telefono = input("Teléfono: ")

            usuario = usuario_crud.crear(
                nombre=nombre,
                apellido=apellido,
                documento=documento,
                correo=correo,
                telefono=telefono,
                fecha_registro=None,
                estado="activo",
            )

            print("\nUsuario creado:")
            print(usuario)

        elif opcion == "2":
            usuarios = usuario_crud.obtener_todos()

            if not usuarios:
                print("\nNo hay usuarios registrados.")
                continue

            for usuario in usuarios:
                print("\n" + str(usuario))

        elif opcion == "3":
            print("Hasta luego.")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()