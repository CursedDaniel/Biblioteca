import uuid
from datetime import date

from src.crud.usuario_crud import UsuarioCrud


def menu_usuarios(usuario_crud: UsuarioCrud):
    while True:
        print("\n--- USUARIOS ---")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Buscar usuario")
        print("4. Actualizar usuario")
        print("5. Eliminar usuario")
        print("0. Volver")

        opcion = input("Seleccione una opción: ").strip()

        # CREAR
        if opcion == "1":
            print("\n--- CREAR USUARIO ---")

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
                fecha_registro=date.today(),
                estado="activo",
            )

            print("\nUsuario creado correctamente.")
            print(usuario)

        # LISTAR
        elif opcion == "2":
            print("\n--- LISTA DE USUARIOS ---")

            usuarios = usuario_crud.obtener_todos()

            if not usuarios:
                print("No hay usuarios registrados.")
                continue

            for usuario in usuarios:
                print("\n" + str(usuario))

        # BUSCAR
        elif opcion == "3":
            print("\n--- BUSCAR USUARIO ---")

            id_texto = input("ID del usuario: ")

            try:
                id_usuario = uuid.UUID(id_texto)
            except ValueError:
                print("El ID ingresado no es válido.")
                continue

            usuario = usuario_crud.obtener_por_id(id_usuario)

            if usuario is None:
                print("Usuario no encontrado.")
            else:
                print("\nUsuario encontrado:")
                print(usuario)

        # ACTUALIZAR
        elif opcion == "4":
            print("\n--- ACTUALIZAR USUARIO ---")

            id_texto = input("ID del usuario: ")

            try:
                id_usuario = uuid.UUID(id_texto)
            except ValueError:
                print("El ID ingresado no es válido.")
                continue

            usuario = usuario_crud.obtener_por_id(id_usuario)

            if usuario is None:
                print("Usuario no encontrado.")
                continue

            print("\nNuevos datos:")

            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            documento = input("Documento: ")
            correo = input("Correo: ")
            telefono = input("Teléfono: ")
            estado = input("Estado: ")

            usuario_crud.actualizar(
                id_usuario=id_usuario,
                nombre=nombre,
                apellido=apellido,
                documento=documento,
                correo=correo,
                telefono=telefono,
                fecha_registro=usuario.fecha_registro,
                estado=estado,
            )

            print("\nUsuario actualizado correctamente.")
            print(usuario)

        # ELIMINAR
        elif opcion == "5":
            print("\n--- ELIMINAR USUARIO ---")

            id_texto = input("ID del usuario: ")

            try:
                id_usuario = uuid.UUID(id_texto)
            except ValueError:
                print("El ID ingresado no es válido.")
                continue

            usuario = usuario_crud.obtener_por_id(id_usuario)

            if usuario is None:
                print("Usuario no encontrado.")
                continue

            print("\nUsuario a eliminar:")
            print(usuario)

            confirmar = input("\n¿Está seguro de eliminarlo? (s/n): ").lower()

            if confirmar == "s":
                usuario_crud.eliminar(id_usuario)
                print("Usuario eliminado correctamente.")
            else:
                print("Operación cancelada.")

        # VOLVER
        elif opcion == "0":
            break

        else:
            print("Opción no válida.")


def main():
    usuario_crud = UsuarioCrud()

    while True:
        print("\n========================")
        print("       BIBLIOTECA")
        print("========================")
        print("1. Usuarios")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_usuarios(usuario_crud)

        elif opcion == "0":
            print("Hasta luego.")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
