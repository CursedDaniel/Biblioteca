import uuid
from datetime import date

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

from src.crud.usuario_crud import UsuarioCrud

# Consola de Rich
console = Console()


# ==========================================================
# FUNCIONES VISUALES
# ==========================================================


def pausar():
    """Pausa la ejecución hasta que el usuario presione ENTER."""
    console.input("\n[dim]Presione ENTER para continuar...[/dim]")


def mostrar_titulo(titulo, subtitulo=None):
    """Muestra un título dentro de un panel."""

    texto = f"[bold cyan]{titulo}[/bold cyan]"

    if subtitulo:
        texto += f"\n[dim]{subtitulo}[/dim]"

    console.print(Panel(texto, expand=False, border_style="cyan"))


def mostrar_error(mensaje):
    """Muestra un mensaje de error."""
    console.print(f"\n[bold red]✗ {mensaje}[/bold red]")


def mostrar_exito(mensaje):
    """Muestra un mensaje de éxito."""
    console.print(f"\n[bold green]✓ {mensaje}[/bold green]")


def obtener_uuid():
    """
    Solicita un UUID al usuario y lo convierte
    de texto a objeto UUID.

    Devuelve:
        uuid.UUID si es válido.
        None si no es válido.
    """

    id_texto = Prompt.ask("[yellow]ID del usuario[/yellow]").strip()

    try:
        return uuid.UUID(id_texto)

    except ValueError:
        mostrar_error("El ID ingresado no es válido.")
        return None


# ==========================================================
# CREAR USUARIO
# ==========================================================


def crear_usuario(usuario_crud):

    console.clear()

    mostrar_titulo("➕ CREAR USUARIO", "Ingrese la información del nuevo usuario")

    nombre = Prompt.ask("Nombre")
    apellido = Prompt.ask("Apellido")
    documento = Prompt.ask("Documento")
    correo = Prompt.ask("Correo")
    telefono = Prompt.ask("Teléfono")

    usuario = usuario_crud.crear(
        nombre=nombre,
        apellido=apellido,
        documento=documento,
        correo=correo,
        telefono=telefono,
        fecha_registro=date.today(),
        estado="activo",
    )

    mostrar_exito("Usuario creado correctamente.")

    console.print(Panel(str(usuario), title="👤 Usuario", border_style="green"))

    pausar()


# ==========================================================
# LISTAR USUARIOS
# ==========================================================


def listar_usuarios(usuario_crud):

    console.clear()

    mostrar_titulo("👥 LISTA DE USUARIOS", "Usuarios registrados en el sistema")

    usuarios = usuario_crud.obtener_todos()

    if not usuarios:
        console.print(
            Panel(
                "[yellow]No hay usuarios registrados.[/yellow]", border_style="yellow"
            )
        )

        pausar()
        return

    tabla = Table(show_lines=True, expand=False)

    tabla.add_column("ID", style="cyan", no_wrap=True)
    tabla.add_column("Nombre")
    tabla.add_column("Apellido")
    tabla.add_column("Documento")
    tabla.add_column("Correo")
    tabla.add_column("Teléfono")
    tabla.add_column("Estado")

    for usuario in usuarios:

        if usuario.estado.lower() == "activo":
            estado = f"[green]● {usuario.estado}[/green]"
        else:
            estado = f"[red]● {usuario.estado}[/red]"

        tabla.add_row(
            str(usuario.id_usuario),
            usuario.nombre,
            usuario.apellido,
            usuario.documento,
            usuario.correo,
            usuario.telefono,
            estado,
        )

    console.print(tabla)

    pausar()


# ==========================================================
# BUSCAR USUARIO
# ==========================================================


def buscar_usuario(usuario_crud):

    console.clear()

    mostrar_titulo("🔍 BUSCAR USUARIO", "Busque un usuario mediante su ID")

    id_usuario = obtener_uuid()

    if id_usuario is None:
        pausar()
        return

    usuario = usuario_crud.obtener_por_id(id_usuario)

    if usuario is None:

        mostrar_error("Usuario no encontrado.")

    else:

        console.print(
            Panel(str(usuario), title="👤 Usuario encontrado", border_style="blue")
        )

    pausar()


# ==========================================================
# ACTUALIZAR USUARIO
# ==========================================================


def actualizar_usuario(usuario_crud):

    console.clear()

    mostrar_titulo("✏️ ACTUALIZAR USUARIO", "Modifique la información del usuario")

    id_usuario = obtener_uuid()

    if id_usuario is None:
        pausar()
        return

    usuario = usuario_crud.obtener_por_id(id_usuario)

    if usuario is None:

        mostrar_error("Usuario no encontrado.")
        pausar()
        return

    console.print(Panel(str(usuario), title="Usuario actual", border_style="yellow"))

    console.print("\n[bold]Ingrese los nuevos datos:[/bold]\n")

    nombre = Prompt.ask("Nombre", default=usuario.nombre)

    apellido = Prompt.ask("Apellido", default=usuario.apellido)

    documento = Prompt.ask("Documento", default=usuario.documento)

    correo = Prompt.ask("Correo", default=usuario.correo)

    telefono = Prompt.ask("Teléfono", default=usuario.telefono)

    estado = Prompt.ask("Estado", default=usuario.estado)

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

    mostrar_exito("Usuario actualizado correctamente.")

    # Volvemos a obtener el usuario actualizado
    usuario_actualizado = usuario_crud.obtener_por_id(id_usuario)

    if usuario_actualizado:
        console.print(
            Panel(
                str(usuario_actualizado),
                title="👤 Usuario actualizado",
                border_style="green",
            )
        )

    pausar()


# ==========================================================
# ELIMINAR USUARIO
# ==========================================================


def eliminar_usuario(usuario_crud):

    console.clear()

    mostrar_titulo("🗑️ ELIMINAR USUARIO", "Esta operación eliminará el registro")

    id_usuario = obtener_uuid()

    if id_usuario is None:
        pausar()
        return

    usuario = usuario_crud.obtener_por_id(id_usuario)

    if usuario is None:

        mostrar_error("Usuario no encontrado.")
        pausar()
        return

    console.print(
        Panel(str(usuario), title="⚠️ Usuario seleccionado", border_style="red")
    )

    confirmar = Confirm.ask(
        "\n[bold red]¿Está seguro de eliminar este usuario?[/bold red]"
    )

    if confirmar:

        usuario_crud.eliminar(id_usuario)

        mostrar_exito("Usuario eliminado correctamente.")

    else:

        console.print("\n[yellow]Operación cancelada.[/yellow]")

    pausar()


# ==========================================================
# MENÚ DE USUARIOS
# ==========================================================


def menu_usuarios(usuario_crud: UsuarioCrud):

    while True:

        console.clear()

        mostrar_titulo("👤 USUARIOS", "Gestión de usuarios")

        console.print(" [bold cyan]1.[/bold cyan] ➕ Crear usuario")
        console.print(" [bold cyan]2.[/bold cyan] 📋 Listar usuarios")
        console.print(" [bold cyan]3.[/bold cyan] 🔍 Buscar usuario")
        console.print(" [bold cyan]4.[/bold cyan] ✏️ Actualizar usuario")
        console.print(" [bold cyan]5.[/bold cyan] 🗑️ Eliminar usuario")
        console.print(" [bold cyan]0.[/bold cyan] ↩ Volver")

        opcion = Prompt.ask(
            "\n[yellow]Seleccione una opción[/yellow]",
            choices=["0", "1", "2", "3", "4", "5"],
        )

        if opcion == "1":
            crear_usuario(usuario_crud)

        elif opcion == "2":
            listar_usuarios(usuario_crud)

        elif opcion == "3":
            buscar_usuario(usuario_crud)

        elif opcion == "4":
            actualizar_usuario(usuario_crud)

        elif opcion == "5":
            eliminar_usuario(usuario_crud)

        elif opcion == "0":
            break


# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================


def main():

    usuario_crud = UsuarioCrud()

    while True:

        console.clear()

        console.print(
            Panel(
                "[bold cyan]📚 BIBLIOTECA[/bold cyan]\n"
                "[dim]Sistema de gestión de biblioteca[/dim]",
                expand=False,
                border_style="cyan",
            )
        )

        console.print("\n[bold]MENÚ PRINCIPAL[/bold]\n")

        console.print(" [cyan]1.[/cyan] 👤 Usuarios")
        console.print(" [cyan]2.[/cyan] 📖 Libros")
        console.print(" [cyan]3.[/cyan] ✍️ Autores")
        console.print(" [cyan]4.[/cyan] 🏷️ Categorías")
        console.print(" [cyan]5.[/cyan] 🏢 Editoriales")
        console.print(" [cyan]6.[/cyan] 📦 Ejemplares")
        console.print(" [cyan]7.[/cyan] 🔄 Préstamos")
        console.print(" [cyan]8.[/cyan] ⚠️ Multas")
        console.print(" [cyan]0.[/cyan] 🚪 Salir")

        opcion = Prompt.ask(
            "\n[yellow]Seleccione una opción[/yellow]",
            choices=["0", "1", "2", "3", "4", "5", "6", "7", "8"],
        )

        if opcion == "1":

            menu_usuarios(usuario_crud)

        elif opcion in ["2", "3", "4", "5", "6", "7", "8"]:

            console.clear()

            console.print(
                Panel(
                    "[yellow]Este módulo todavía está en desarrollo.[/yellow]",
                    title="🚧 Próximamente",
                    border_style="yellow",
                )
            )

            pausar()

        elif opcion == "0":

            console.clear()

            console.print(
                Panel(
                    "[bold cyan]📚 Gracias por utilizar la Biblioteca[/bold cyan]\n"
                    "[dim]Hasta luego.[/dim]",
                    expand=False,
                    border_style="cyan",
                )
            )

            break


# ==========================================================
# EJECUCIÓN
# ==========================================================

if __name__ == "__main__":
    main()
