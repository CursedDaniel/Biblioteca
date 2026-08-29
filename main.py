import uuid

from datetime import date, datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

from src.crud.ejemplar_crud import EjemplarCrud
from src.crud.libro_crud import LibroCrud
from src.crud.usuario_crud import UsuarioCrud
from src.crud.libro_crud import LibroCrud
from src.crud.autor_crud import AutorCrud
from src.crud.categoria_crud import CategoriaCrud
from src.crud.editorial_crud import EditorialCrud
from src.crud.ejemplar_crud import EjemplarCrud
from src.crud.prestamo_crud import PrestamoCrud
from src.crud.multa_crud import MultaCrud

from src.crud.categoria_crud import CategoriaCrud
from src.crud.multa_crud import MultaCrud
from datos_prueba import cargar_datos_prueba

console = Console()


# ==========================================================
# FUNCIONES GENERALES
# ==========================================================


def pausar():
    console.input("\n[dim]Presione ENTER para continuar...[/dim]")


def mostrar_titulo(titulo, subtitulo=None):
    texto = f"[bold cyan]{titulo}[/bold cyan]"

    if subtitulo:
        texto += f"\n[dim]{subtitulo}[/dim]"

    console.print(Panel(texto, expand=False, border_style="cyan"))


def mostrar_error(mensaje):
    console.print(f"\n[bold red]✗ {mensaje}[/bold red]")


def mostrar_exito(mensaje):
    console.print(f"\n[bold green]✓ {mensaje}[/bold green]")


def obtener_uuid(mensaje="ID"):
    texto = Prompt.ask(f"[yellow]{mensaje}[/yellow]").strip()

    try:
        return uuid.UUID(texto)

    except ValueError:
        mostrar_error("El ID ingresado no es válido.")
        return None


def buscar_prestamo_por_documento_y_codigo(prestamo_crud, usuario_crud, ejemplar_crud):
    documento = Prompt.ask("Documento del usuario")

    usuario = usuario_crud.obtener_por_documento(documento)

    if usuario is None:
        mostrar_error("Usuario no encontrado.")
        return None

    codigo_inventario = Prompt.ask("Código de inventario del ejemplar")

    ejemplar = ejemplar_crud.obtener_por_codigo_inventario(codigo_inventario)

    if ejemplar is None:
        mostrar_error("Ejemplar no encontrado.")
        return None

    coincidencias = prestamo_crud.obtener_por_usuario_y_ejemplar(
        usuario.id_usuario, ejemplar.id_ejemplar
    )

    if not coincidencias:
        mostrar_error("No se encontró ningún préstamo con esos datos.")
        return None

    if len(coincidencias) == 1:
        return coincidencias[0]

    console.print(
        "\n[yellow]Hay varios préstamos para ese usuario y ejemplar:[/yellow]"
    )

    tabla = Table(show_lines=True)
    tabla.add_column("Fecha préstamo", style="cyan")
    tabla.add_column("Fecha límite")
    tabla.add_column("Estado")

    for prestamo in coincidencias:
        tabla.add_row(
            str(prestamo.fecha_prestamo),
            str(prestamo.fecha_limite),
            prestamo.estado,
        )

    console.print(tabla)

    fecha_prestamo = obtener_fecha("Fecha del préstamo a seleccionar")

    if fecha_prestamo is None:
        return None

    for prestamo in coincidencias:
        if prestamo.fecha_prestamo == fecha_prestamo:
            return prestamo

    mostrar_error("No se encontró un préstamo con esa fecha exacta.")
    return None


def obtener_fecha(mensaje):
    texto = Prompt.ask(f"[yellow]{mensaje} (AAAA-MM-DD)[/yellow]").strip()

    try:
        return datetime.strptime(texto, "%Y-%m-%d").date()

    except ValueError:
        mostrar_error("La fecha no es válida. Use el formato AAAA-MM-DD.")
        return None


def obtener_entero(mensaje):
    texto = Prompt.ask(f"[yellow]{mensaje}[/yellow]").strip()

    try:
        return int(texto)

    except ValueError:
        mostrar_error("Debe ingresar un número entero.")
        return None


# ==========================================================
# USUARIOS
# ==========================================================


def menu_usuarios(usuario_crud):

    while True:

        console.clear()

        mostrar_titulo("👤 USUARIOS", "Gestión de usuarios")

        console.print(" [cyan]1.[/cyan] ➕ Crear usuario")
        console.print(" [cyan]2.[/cyan] 📋 Listar usuarios")
        console.print(" [cyan]3.[/cyan] 🔍 Buscar usuario")
        console.print(" [cyan]4.[/cyan] ✏️ Actualizar usuario")
        console.print(" [cyan]5.[/cyan] 🗑️ Eliminar usuario")
        console.print(" [cyan]0.[/cyan] ↩ Volver")

        opcion = Prompt.ask(
            "\n[yellow]Seleccione una opción[/yellow]",
            choices=["0", "1", "2", "3", "4", "5"],
        )

        if opcion == "1":

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

        elif opcion == "2":

            usuarios = usuario_crud.obtener_todos()

            if not usuarios:

                console.print(
                    Panel(
                        "[yellow]No hay usuarios registrados.[/yellow]",
                        border_style="yellow",
                    )
                )

            else:

                tabla = Table(show_lines=True, expand=False)

                tabla.add_column("ID", style="cyan")
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

        elif opcion == "3":

            id_usuario = obtener_uuid("ID del usuario")

            if id_usuario:

                usuario = usuario_crud.obtener_por_id(id_usuario)

                if usuario is None:

                    mostrar_error("Usuario no encontrado.")

                else:

                    console.print(
                        Panel(
                            str(usuario),
                            title="👤 Usuario encontrado",
                            border_style="blue",
                        )
                    )

            pausar()

        elif opcion == "4":

            documento = Prompt.ask("Documento del usuario")

            usuario = usuario_crud.obtener_por_documento(documento)

            if usuario is None:

                mostrar_error("Usuario no encontrado.")

            else:

                console.print(
                    Panel(
                        "[bold cyan]✏️ ACTUALIZAR USUARIO[/bold cyan]",
                        expand=False,
                        border_style="cyan",
                    )
                )

                nombre = Prompt.ask("Nombre", default=usuario.nombre)

                apellido = Prompt.ask("Apellido", default=usuario.apellido)

                nuevo_documento = Prompt.ask("Documento", default=usuario.documento)

                correo = Prompt.ask("Correo", default=usuario.correo)

                telefono = Prompt.ask("Teléfono", default=usuario.telefono)

                console.print("\n[bold cyan]Estado del usuario[/bold cyan]")

                console.print(" [cyan]1.[/cyan] Activo")
                console.print(" [cyan]2.[/cyan] Inactivo")
                console.print(" [cyan]3.[/cyan] Suspendido")

                opcion_estado = Prompt.ask(
                    "\n[yellow]Seleccione el estado[/yellow]",
                    choices=["1", "2", "3"],
                )

                estados = {
                    "1": "activo",
                    "2": "inactivo",
                    "3": "suspendido",
                }

                estado = estados[opcion_estado]

                usuario_crud.actualizar(
                    id_usuario=usuario.id_usuario,
                    nombre=nombre,
                    apellido=apellido,
                    documento=nuevo_documento,
                    correo=correo,
                    telefono=telefono,
                    fecha_registro=usuario.fecha_registro,
                    estado=estado,
                )

                mostrar_exito("Usuario actualizado correctamente.")

                usuario_actualizado = usuario_crud.obtener_por_id(usuario.id_usuario)

                console.print(
                    Panel(
                        str(usuario_actualizado),
                        title="👤 Usuario actualizado",
                        border_style="green",
                    )
                )

            pausar()

        elif opcion == "5":

            id_usuario = obtener_uuid("ID del usuario")

            if id_usuario:

                usuario = usuario_crud.obtener_por_id(id_usuario)

                if usuario is None:

                    mostrar_error("Usuario no encontrado.")

                else:

                    confirmar = Confirm.ask("¿Está seguro de eliminar este usuario?")

                    if confirmar:

                        if usuario_crud.eliminar(id_usuario):
                            mostrar_exito("Usuario eliminado correctamente.")
                        else:
                            mostrar_error("No se pudo eliminar el usuario.")

                    else:

                        console.print("[yellow]Operación cancelada.[/yellow]")

            pausar()

        elif opcion == "0":
            break


# ==========================================================
# AUTORES
# ==========================================================


def menu_autores(autor_crud):

    while True:

        console.clear()

        mostrar_titulo("✍️ AUTORES", "Gestión de autores")

        console.print(" [cyan]1.[/cyan] ➕ Crear autor")
        console.print(" [cyan]2.[/cyan] 📋 Listar autores")
        console.print(" [cyan]3.[/cyan] 🔍 Buscar autor")
        console.print(" [cyan]4.[/cyan] ✏️ Actualizar autor")
        console.print(" [cyan]5.[/cyan] 🗑️ Eliminar autor")
        console.print(" [cyan]0.[/cyan] ↩ Volver")

        opcion = Prompt.ask(
            "\n[yellow]Seleccione una opción[/yellow]",
            choices=["0", "1", "2", "3", "4", "5"],
        )

        if opcion == "1":

            nombre = Prompt.ask("Nombre")
            apellido = Prompt.ask("Apellido")

            fecha_nacimiento = obtener_fecha("Fecha de nacimiento")

            if fecha_nacimiento is None:
                pausar()
                continue

            nacionalidad = Prompt.ask("Nacionalidad")

            biografia = Prompt.ask("Biografía")

            autor = autor_crud.crear(
                nombre=nombre,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento,
                nacionalidad=nacionalidad,
                biografia=biografia,
            )

            mostrar_exito("Autor creado correctamente.")

            console.print(Panel(str(autor), title="✍️ Autor", border_style="green"))

            pausar()

        elif opcion == "2":

            autores = autor_crud.obtener_todos()

            if not autores:

                console.print("[yellow]No hay autores registrados.[/yellow]")

            else:

                tabla = Table(show_lines=True)

                tabla.add_column("ID", style="cyan")
                tabla.add_column("Nombre")
                tabla.add_column("Apellido")
                tabla.add_column("Nacimiento")
                tabla.add_column("Nacionalidad")

                for autor in autores:

                    tabla.add_row(
                        str(autor.id_autor),
                        autor.nombre,
                        autor.apellido,
                        str(autor.fecha_nacimiento),
                        autor.nacionalidad,
                    )

                console.print(tabla)

            pausar()

        elif opcion == "3":

            id_autor = obtener_uuid("ID del autor")

            if id_autor:

                autor = autor_crud.obtener_por_id(id_autor)

                if autor is None:

                    mostrar_error("Autor no encontrado.")

                else:

                    console.print(
                        Panel(
                            str(autor), title="✍️ Autor encontrado", border_style="blue"
                        )
                    )

            pausar()

        elif opcion == "4":

            id_autor = obtener_uuid("ID del autor")

            if id_autor:

                autor = autor_crud.obtener_por_id(id_autor)

                if autor is None:

                    mostrar_error("Autor no encontrado.")

                else:

                    nombre = Prompt.ask("Nombre", default=autor.nombre)

                    apellido = Prompt.ask("Apellido", default=autor.apellido)

                    fecha_nacimiento = obtener_fecha("Nueva fecha de nacimiento")

                    if fecha_nacimiento is not None:

                        nacionalidad = Prompt.ask(
                            "Nacionalidad", default=autor.nacionalidad
                        )

                        biografia = Prompt.ask("Biografía", default=autor.biografia)

                        autor_crud.actualizar(
                            id_autor=id_autor,
                            nombre=nombre,
                            apellido=apellido,
                            fecha_nacimiento=fecha_nacimiento,
                            nacionalidad=nacionalidad,
                            biografia=biografia,
                        )

                        mostrar_exito("Autor actualizado correctamente.")

            pausar()

        elif opcion == "5":

            id_autor = obtener_uuid("ID del autor")

            if id_autor:

                autor = autor_crud.obtener_por_id(id_autor)

                if autor is None:

                    mostrar_error("Autor no encontrado.")

                else:

                    confirmar = Confirm.ask("¿Está seguro de eliminar este autor?")

                    if confirmar:

                        if autor_crud.eliminar(id_autor):
                            mostrar_exito("Autor eliminado correctamente.")
                        else:
                            mostrar_error("No se pudo eliminar el autor.")

            pausar()

        elif opcion == "0":
            break


# ==========================================================
# CATEGORÍAS
# ==========================================================


def menu_categorias(categoria_crud):

    while True:

        console.clear()

        mostrar_titulo("🏷️ CATEGORÍAS", "Gestión de categorías")

        console.print(" [cyan]1.[/cyan] ➕ Crear categoría")
        console.print(" [cyan]2.[/cyan] 📋 Listar categorías")
        console.print(" [cyan]3.[/cyan] 🔍 Buscar categoría")
        console.print(" [cyan]4.[/cyan] ✏️ Actualizar categoría")
        console.print(" [cyan]5.[/cyan] 🗑️ Eliminar categoría")
        console.print(" [cyan]0.[/cyan] ↩ Volver")

        opcion = Prompt.ask(
            "\n[yellow]Seleccione una opción[/yellow]",
            choices=["0", "1", "2", "3", "4", "5"],
        )

        if opcion == "1":

            nombre = Prompt.ask("Nombre")
            descripcion = Prompt.ask("Descripción")

            categoria = categoria_crud.crear(
                nombre=nombre,
                descripcion=descripcion,
            )

            mostrar_exito("Categoría creada correctamente.")

            console.print(
                Panel(str(categoria), title="🏷️ Categoría", border_style="green")
            )

            pausar()

        elif opcion == "2":

            categorias = categoria_crud.obtener_todos()

            if not categorias:

                console.print("[yellow]No hay categorías registradas.[/yellow]")

            else:

                tabla = Table(show_lines=True)

                tabla.add_column("ID", style="cyan")
                tabla.add_column("Nombre")
                tabla.add_column("Descripción")

                for categoria in categorias:

                    tabla.add_row(
                        str(categoria.id_categoria),
                        categoria.nombre,
                        categoria.descripcion,
                    )

                console.print(tabla)

            pausar()

        elif opcion == "3":

            nombre = Prompt.ask("Nombre de la categoría")

            categoria = categoria_crud.obtener_por_nombre(nombre)

            if categoria is None:

                mostrar_error("Categoría no encontrada.")

            else:

                console.print(
                    Panel(
                        str(categoria),
                        title="🏷️ Categoría encontrada",
                        border_style="blue",
                    )
                )

            pausar()

        elif opcion == "4":

            nombre = Prompt.ask("Nombre de la categoría")

            categoria = categoria_crud.obtener_por_nombre(nombre)

            if categoria is None:

                mostrar_error("Categoría no encontrada.")

            else:

                nuevo_nombre = Prompt.ask("Nombre", default=categoria.nombre)

                descripcion = Prompt.ask("Descripción", default=categoria.descripcion)

                categoria_crud.actualizar(
                    id_categoria=categoria.id_categoria,
                    nombre=nuevo_nombre,
                    descripcion=descripcion,
                )

                mostrar_exito("Categoría actualizada correctamente.")

            pausar()

        elif opcion == "5":

            nombre = Prompt.ask("Nombre de la categoría")

            categoria = categoria_crud.obtener_por_nombre(nombre)

            if categoria is None:

                mostrar_error("Categoría no encontrada.")

            else:

                confirmar = Confirm.ask("¿Está seguro de eliminar esta categoría?")

                if confirmar:

                    if categoria_crud.eliminar(categoria.id_categoria):
                        mostrar_exito("Categoría eliminada correctamente.")
                    else:
                        mostrar_error("No se pudo eliminar la categoría.")

            pausar()

        elif opcion == "0":
            break


# ==========================================================
# EDITORIALES
# ==========================================================


def menu_editoriales(editorial_crud):

    while True:

        console.clear()

        mostrar_titulo("🏢 EDITORIALES", "Gestión de editoriales")

        console.print(" [cyan]1.[/cyan] ➕ Crear editorial")
        console.print(" [cyan]2.[/cyan] 📋 Listar editoriales")
        console.print(" [cyan]3.[/cyan] 🔍 Buscar editorial")
        console.print(" [cyan]4.[/cyan] ✏️ Actualizar editorial")
        console.print(" [cyan]5.[/cyan] 🗑️ Eliminar editorial")
        console.print(" [cyan]0.[/cyan] ↩ Volver")

        opcion = Prompt.ask(
            "\n[yellow]Seleccione una opción[/yellow]",
            choices=["0", "1", "2", "3", "4", "5"],
        )

        if opcion == "1":

            nombre = Prompt.ask("Nombre")
            pais = Prompt.ask("País")
            ciudad = Prompt.ask("Ciudad")
            telefono = Prompt.ask("Teléfono")
            correo = Prompt.ask("Correo")

            editorial = editorial_crud.crear(
                nombre=nombre,
                pais=pais,
                ciudad=ciudad,
                telefono=telefono,
                correo=correo,
            )

            mostrar_exito("Editorial creada correctamente.")

            console.print(
                Panel(str(editorial), title="🏢 Editorial", border_style="green")
            )

            pausar()

        elif opcion == "2":

            editoriales = editorial_crud.obtener_todos()

            if not editoriales:

                console.print("[yellow]No hay editoriales registradas.[/yellow]")

            else:

                tabla = Table(show_lines=True)

                tabla.add_column("ID", style="cyan")
                tabla.add_column("Nombre")
                tabla.add_column("País")
                tabla.add_column("Ciudad")
                tabla.add_column("Teléfono")
                tabla.add_column("Correo")

                for editorial in editoriales:

                    tabla.add_row(
                        str(editorial.id_editorial),
                        editorial.nombre,
                        editorial.pais,
                        editorial.ciudad,
                        editorial.telefono,
                        editorial.correo,
                    )

                console.print(tabla)

            pausar()

        elif opcion == "3":

            nombre = Prompt.ask("Nombre de la editorial")

            editorial = editorial_crud.obtener_por_nombre(nombre)

            if editorial is None:

                mostrar_error("Editorial no encontrada.")

            else:

                console.print(
                    Panel(
                        str(editorial),
                        title="🏢 Editorial encontrada",
                        border_style="blue",
                    )
                )

            pausar()

        elif opcion == "4":

            nombre = Prompt.ask("Nombre de la editorial")

            editorial = editorial_crud.obtener_por_nombre(nombre)

            if editorial is None:

                mostrar_error("Editorial no encontrada.")

            else:

                nuevo_nombre = Prompt.ask("Nombre", default=editorial.nombre)

                pais = Prompt.ask("País", default=editorial.pais)

                ciudad = Prompt.ask("Ciudad", default=editorial.ciudad)

                telefono = Prompt.ask("Teléfono", default=editorial.telefono)

                correo = Prompt.ask("Correo", default=editorial.correo)

                editorial_crud.actualizar(
                    id_editorial=editorial.id_editorial,
                    nombre=nuevo_nombre,
                    pais=pais,
                    ciudad=ciudad,
                    telefono=telefono,
                    correo=correo,
                )

                mostrar_exito("Editorial actualizada correctamente.")

            pausar()

        elif opcion == "5":

            nombre = Prompt.ask("Nombre de la editorial")

            editorial = editorial_crud.obtener_por_nombre(nombre)

            if editorial is None:

                mostrar_error("Editorial no encontrada.")

            else:

                confirmar = Confirm.ask("¿Está seguro de eliminar esta editorial?")

                if confirmar:

                    if editorial_crud.eliminar(editorial.id_editorial):
                        mostrar_exito("Editorial eliminada correctamente.")
                    else:
                        mostrar_error("No se pudo eliminar la editorial.")

            pausar()

        elif opcion == "0":
            break


# ==========================================================
# LIBROS
# ==========================================================


def menu_libros(libro_crud, categoria_crud, editorial_crud):

    while True:

        console.clear()

        mostrar_titulo("📖 LIBROS", "Gestión de libros")

        console.print(" [cyan]1.[/cyan] ➕ Crear libro")
        console.print(" [cyan]2.[/cyan] 📋 Listar libros")
        console.print(" [cyan]3.[/cyan] 🔍 Buscar libro")
        console.print(" [cyan]4.[/cyan] ✏️ Actualizar libro")
        console.print(" [cyan]5.[/cyan] 🗑️ Eliminar libro")
        console.print(" [cyan]0.[/cyan] ↩ Volver")

        opcion = Prompt.ask(
            "\n[yellow]Seleccione una opción[/yellow]",
            choices=["0", "1", "2", "3", "4", "5"],
        )

        if opcion == "1":

            titulo = Prompt.ask("Título")

            fecha_publicacion = obtener_fecha("Fecha de publicación")

            numero_paginas = obtener_entero("Número de páginas")

            if fecha_publicacion is None or numero_paginas is None:
                pausar()
                continue

            idiomas = Prompt.ask("Idioma")
            descripcion = Prompt.ask("Descripción")

            nombre_categoria = Prompt.ask("Nombre de la categoría")
            categoria = categoria_crud.obtener_por_nombre(nombre_categoria)

            if categoria is None:
                mostrar_error("Categoría no encontrada.")
                pausar()
                continue

            nombre_editorial = Prompt.ask("Nombre de la editorial")
            editorial = editorial_crud.obtener_por_nombre(nombre_editorial)

            if editorial is None:
                mostrar_error("Editorial no encontrada.")
                pausar()
                continue

            libro = libro_crud.crear(
                titulo=titulo,
                fecha_publicacion=fecha_publicacion,
                numero_paginas=numero_paginas,
                idiomas=idiomas,
                descripcion=descripcion,
                id_categoria=categoria.id_categoria,
                id_editorial=editorial.id_editorial,
            )

            mostrar_exito("Libro creado correctamente.")

            console.print(Panel(str(libro), title="📖 Libro", border_style="green"))

            pausar()

        elif opcion == "2":

            libros = libro_crud.obtener_todos()

            if not libros:

                console.print("[yellow]No hay libros registrados.[/yellow]")

            else:

                tabla = Table(show_lines=True)

                tabla.add_column("ID", style="cyan")
                tabla.add_column("Título")
                tabla.add_column("Publicación")
                tabla.add_column("Páginas")
                tabla.add_column("Idiomas")
                tabla.add_column("Categoría")
                tabla.add_column("Editorial")

                for libro in libros:

                    categoria = categoria_crud.obtener_por_id(libro.id_categoria)
                    editorial = editorial_crud.obtener_por_id(libro.id_editorial)

                    nombre_categoria = categoria.nombre if categoria else "—"
                    nombre_editorial = editorial.nombre if editorial else "—"

                    tabla.add_row(
                        str(libro.id_libro),
                        libro.titulo,
                        str(libro.fecha_publicacion),
                        str(libro.numero_paginas),
                        libro.idiomas,
                        nombre_categoria,
                        nombre_editorial,
                    )

                console.print(tabla)

            pausar()

        elif opcion == "3":

            titulo = Prompt.ask("Título del libro")

            libro = libro_crud.obtener_por_titulo(titulo)

            if libro is None:

                mostrar_error("Libro no encontrado.")

            else:

                console.print(
                    Panel(str(libro), title="📖 Libro encontrado", border_style="blue")
                )

            pausar()

        elif opcion == "4":

            titulo = Prompt.ask("Título del libro")

            libro = libro_crud.obtener_por_titulo(titulo)

            if libro is None:

                mostrar_error("Libro no encontrado.")

            else:

                nuevo_titulo = Prompt.ask("Título", default=libro.titulo)

                fecha_publicacion = obtener_fecha("Nueva fecha de publicación")

                numero_paginas = obtener_entero("Número de páginas")

                if fecha_publicacion is not None and numero_paginas is not None:

                    idiomas = Prompt.ask("Idiomas", default=libro.idiomas)

                    descripcion = Prompt.ask("Descripción", default=libro.descripcion)

                    categoria_actual = categoria_crud.obtener_por_id(libro.id_categoria)
                    nombre_categoria = Prompt.ask(
                        "Nombre de la categoría",
                        default=categoria_actual.nombre if categoria_actual else "",
                    )
                    categoria = categoria_crud.obtener_por_nombre(nombre_categoria)

                    editorial_actual = editorial_crud.obtener_por_id(libro.id_editorial)
                    nombre_editorial = Prompt.ask(
                        "Nombre de la editorial",
                        default=editorial_actual.nombre if editorial_actual else "",
                    )
                    editorial = editorial_crud.obtener_por_nombre(nombre_editorial)

                    if categoria is None:
                        mostrar_error("Categoría no encontrada.")
                        pausar()
                        continue

                    if editorial is None:
                        mostrar_error("Editorial no encontrada.")
                        pausar()
                        continue

                    libro_crud.actualizar(
                        id_libro=libro.id_libro,
                        titulo=nuevo_titulo,
                        fecha_publicacion=fecha_publicacion,
                        numero_paginas=numero_paginas,
                        idiomas=idiomas,
                        descripcion=descripcion,
                        id_categoria=categoria.id_categoria,
                        id_editorial=editorial.id_editorial,
                    )

                    mostrar_exito("Libro actualizado correctamente.")

            pausar()

        elif opcion == "5":

            titulo = Prompt.ask("Título del libro")

            libro = libro_crud.obtener_por_titulo(titulo)

            if libro is None:

                mostrar_error("Libro no encontrado.")

            else:

                confirmar = Confirm.ask("¿Está seguro de eliminar este libro?")

                if confirmar:

                    if libro_crud.eliminar(libro.id_libro):
                        mostrar_exito("Libro eliminado correctamente.")
                    else:
                        mostrar_error("No se pudo eliminar el libro.")

            pausar()

        elif opcion == "0":
            break


# ==========================================================
# EJEMPLARES
# ==========================================================


def menu_ejemplares(ejemplar_crud, libro_crud):

    while True:

        console.clear()

        mostrar_titulo("📦 EJEMPLARES", "Gestión de ejemplares")

        console.print(" [cyan]1.[/cyan] ➕ Crear ejemplar")
        console.print(" [cyan]2.[/cyan] 📋 Listar ejemplares")
        console.print(" [cyan]3.[/cyan] 🔍 Buscar ejemplar")
        console.print(" [cyan]4.[/cyan] ✏️ Actualizar ejemplar")
        console.print(" [cyan]5.[/cyan] 🗑️ Eliminar ejemplar")
        console.print(" [cyan]0.[/cyan] ↩ Volver")

        opcion = Prompt.ask(
            "\n[yellow]Seleccione una opción[/yellow]",
            choices=["0", "1", "2", "3", "4", "5"],
        )

        if opcion == "1":

            titulo_libro = Prompt.ask("Título del libro")

            libro = libro_crud.obtener_por_titulo(titulo_libro)

            if libro is None:
                mostrar_error("Libro no encontrado.")
                pausar()
                continue

            codigo_inventario = Prompt.ask("Código de inventario")

            fecha_adquisicion = obtener_fecha("Fecha de adquisición")

            if fecha_adquisicion is None:
                pausar()
                continue

            estado = Prompt.ask("Estado")
            ubicacion = Prompt.ask("Ubicación")

            ejemplar = ejemplar_crud.crear(
                id_libro=libro.id_libro,
                codigo_inventario=codigo_inventario,
                fecha_adquisicion=fecha_adquisicion,
                estado=estado,
                ubicacion=ubicacion,
            )

            mostrar_exito("Ejemplar creado correctamente.")

            console.print(
                Panel(str(ejemplar), title="📦 Ejemplar", border_style="green")
            )

            pausar()

        elif opcion == "2":

            ejemplares = ejemplar_crud.obtener_todos()

            if not ejemplares:

                console.print("[yellow]No hay ejemplares registrados.[/yellow]")

            else:

                tabla = Table(show_lines=True)

                tabla.add_column("ID", style="cyan")
                tabla.add_column("Libro")
                tabla.add_column("Inventario")
                tabla.add_column("Adquisición")
                tabla.add_column("Estado")
                tabla.add_column("Ubicación")

                for ejemplar in ejemplares:

                    libro = libro_crud.obtener_por_id(ejemplar.id_libro)
                    titulo_libro = libro.titulo if libro else "—"

                    tabla.add_row(
                        str(ejemplar.id_ejemplar),
                        titulo_libro,
                        ejemplar.codigo_inventario,
                        str(ejemplar.fecha_adquisicion),
                        ejemplar.estado,
                        ejemplar.ubicacion,
                    )

                console.print(tabla)

            pausar()

        elif opcion == "3":

            codigo_inventario = Prompt.ask("Código de inventario")

            ejemplar = ejemplar_crud.obtener_por_codigo_inventario(codigo_inventario)

            if ejemplar is None:

                mostrar_error("Ejemplar no encontrado.")

            else:

                console.print(
                    Panel(
                        str(ejemplar),
                        title="📦 Ejemplar encontrado",
                        border_style="blue",
                    )
                )

            pausar()

        elif opcion == "4":

            codigo_inventario = Prompt.ask("Código de inventario")

            ejemplar = ejemplar_crud.obtener_por_codigo_inventario(codigo_inventario)

            if ejemplar is None:

                mostrar_error("Ejemplar no encontrado.")

            else:

                libro_actual = libro_crud.obtener_por_id(ejemplar.id_libro)

                titulo_libro = Prompt.ask(
                    "Título del libro",
                    default=libro_actual.titulo if libro_actual else "",
                )

                libro = libro_crud.obtener_por_titulo(titulo_libro)

                if libro is None:
                    mostrar_error("Libro no encontrado.")
                    pausar()
                    continue

                nuevo_codigo = Prompt.ask(
                    "Código de inventario", default=ejemplar.codigo_inventario
                )

                fecha_adquisicion = obtener_fecha("Fecha de adquisición")

                if fecha_adquisicion is None:
                    pausar()
                    continue

                estado = Prompt.ask("Estado", default=ejemplar.estado)

                ubicacion = Prompt.ask("Ubicación", default=ejemplar.ubicacion)

                ejemplar_crud.actualizar(
                    id_ejemplar=ejemplar.id_ejemplar,
                    id_libro=libro.id_libro,
                    codigo_inventario=nuevo_codigo,
                    fecha_adquisicion=fecha_adquisicion,
                    estado=estado,
                    ubicacion=ubicacion,
                )

                mostrar_exito("Ejemplar actualizado correctamente.")

            pausar()

        elif opcion == "5":

            codigo_inventario = Prompt.ask("Código de inventario")

            ejemplar = ejemplar_crud.obtener_por_codigo_inventario(codigo_inventario)

            if ejemplar is None:

                mostrar_error("Ejemplar no encontrado.")

            else:

                confirmar = Confirm.ask("¿Está seguro de eliminar este ejemplar?")

                if confirmar:

                    if ejemplar_crud.eliminar(ejemplar.id_ejemplar):
                        mostrar_exito("Ejemplar eliminado correctamente.")
                    else:
                        mostrar_error("No se pudo eliminar el ejemplar.")

            pausar()

        elif opcion == "0":
            break


# ==========================================================
# PRÉSTAMOS
# ==========================================================


def menu_prestamos(prestamo_crud, usuario_crud, ejemplar_crud, libro_crud):

    while True:

        console.clear()

        mostrar_titulo("🔄 PRÉSTAMOS", "Gestión de préstamos")

        console.print(" [cyan]1.[/cyan] ➕ Crear préstamo")
        console.print(" [cyan]2.[/cyan] 📋 Listar préstamos")
        console.print(" [cyan]3.[/cyan] 🔍 Buscar préstamo")
        console.print(" [cyan]4.[/cyan] ✏️ Actualizar préstamo")
        console.print(" [cyan]5.[/cyan] 🗑️ Eliminar préstamo")
        console.print(" [cyan]0.[/cyan] ↩ Volver")

        opcion = Prompt.ask(
            "\n[yellow]Seleccione una opción[/yellow]",
            choices=["0", "1", "2", "3", "4", "5"],
        )

        if opcion == "1":

            documento_usuario = Prompt.ask("Documento del usuario")

            usuario = usuario_crud.obtener_por_documento(documento_usuario)

            if usuario is None:

                mostrar_error("Usuario no encontrado.")

                pausar()
                continue

            codigo_inventario = Prompt.ask("Código de inventario del ejemplar")

            ejemplar = ejemplar_crud.obtener_por_codigo_inventario(codigo_inventario)

            if ejemplar is None:

                mostrar_error("Ejemplar no encontrado.")

                pausar()
                continue

            fecha_prestamo = obtener_fecha("Fecha del préstamo")

            fecha_limite = obtener_fecha("Fecha límite")

            if fecha_prestamo is None or fecha_limite is None:
                pausar()
                continue

            prestamo = prestamo_crud.crear(
                id_usuario=usuario.id_usuario,
                id_ejemplar=ejemplar.id_ejemplar,
                fecha_prestamo=fecha_prestamo,
                fecha_limite=fecha_limite,
            )

            mostrar_exito("Préstamo creado correctamente.")

            console.print(
                Panel(str(prestamo), title="🔄 Préstamo", border_style="green")
            )

            pausar()

        elif opcion == "2":

            prestamos = prestamo_crud.obtener_todos()

            if not prestamos:

                console.print("[yellow]No hay préstamos registrados.[/yellow]")

            else:

                tabla = Table(show_lines=True)

                tabla.add_column("ID", style="cyan")
                tabla.add_column("Usuario")
                tabla.add_column("Ejemplar")
                tabla.add_column("Préstamo")
                tabla.add_column("Límite")
                tabla.add_column("Devolución")
                tabla.add_column("Estado")

                for prestamo in prestamos:

                    usuario = usuario_crud.obtener_por_id(prestamo.id_usuario)
                    ejemplar = ejemplar_crud.obtener_por_id(prestamo.id_ejemplar)

                    if usuario:
                        texto_usuario = f"{usuario.documento} - {usuario.nombre}"
                    else:
                        texto_usuario = "—"

                    if ejemplar:
                        libro = libro_crud.obtener_por_id(ejemplar.id_libro)
                        titulo_libro = libro.titulo if libro else "—"
                        texto_ejemplar = (
                            f"{ejemplar.codigo_inventario} - {titulo_libro}"
                        )
                    else:
                        texto_ejemplar = "—"

                    tabla.add_row(
                        str(prestamo.id_prestamo),
                        texto_usuario,
                        texto_ejemplar,
                        str(prestamo.fecha_prestamo),
                        str(prestamo.fecha_limite),
                        str(prestamo.fecha_devolucion),
                        prestamo.estado,
                    )

                console.print(tabla)

            pausar()

        elif opcion == "3":

            prestamo = buscar_prestamo_por_documento_y_codigo(
                prestamo_crud, usuario_crud, ejemplar_crud
            )

            if prestamo is not None:

                console.print(
                    Panel(
                        str(prestamo),
                        title="🔄 Préstamo encontrado",
                        border_style="blue",
                    )
                )

            pausar()

        elif opcion == "4":

            prestamo = buscar_prestamo_por_documento_y_codigo(
                prestamo_crud, usuario_crud, ejemplar_crud
            )

            if prestamo is not None:

                nueva_fecha_limite = obtener_fecha("Nueva fecha límite")

                if nueva_fecha_limite is None:
                    pausar()
                    continue

                texto_devolucion = Prompt.ask(
                    "Fecha de devolución (AAAA-MM-DD, vacío si no se ha devuelto)",
                    default="",
                )

                fecha_devolucion = None

                if texto_devolucion.strip():

                    try:

                        fecha_devolucion = datetime.strptime(
                            texto_devolucion, "%Y-%m-%d"
                        ).date()

                    except ValueError:

                        mostrar_error("Fecha de devolución inválida.")

                        pausar()
                        continue

                estado = Prompt.ask("Estado", default=prestamo.estado)

                prestamo_crud.actualizar(
                    id_prestamo=prestamo.id_prestamo,
                    id_usuario=prestamo.id_usuario,
                    id_ejemplar=prestamo.id_ejemplar,
                    fecha_prestamo=prestamo.fecha_prestamo,
                    fecha_limite=nueva_fecha_limite,
                    fecha_devolucion=fecha_devolucion,
                    estado=estado,
                )

                mostrar_exito("Préstamo actualizado correctamente.")

            pausar()

        elif opcion == "5":

            prestamo = buscar_prestamo_por_documento_y_codigo(
                prestamo_crud, usuario_crud, ejemplar_crud
            )

            if prestamo is not None:

                confirmar = Confirm.ask("¿Está seguro de eliminar este préstamo?")

                if confirmar:

                    if prestamo_crud.eliminar(prestamo.id_prestamo):
                        mostrar_exito("Préstamo eliminado correctamente.")
                    else:
                        mostrar_error("No se pudo eliminar el préstamo.")

            pausar()

        elif opcion == "0":
            break


# ==========================================================
# MULTAS
# ==========================================================


def menu_multas(multa_crud, prestamo_crud):

    while True:

        console.clear()

        mostrar_titulo("⚠️ MULTAS ", "Gestión de multas")

        console.print(" [cyan]1.[/cyan] ➕ Crear multa")
        console.print(" [cyan]2.[/cyan] 📋 Listar multas")
        console.print(" [cyan]3.[/cyan] 🔍 Buscar multa")
        console.print(" [cyan]4.[/cyan] ✏️ Actualizar multa")
        console.print(" [cyan]5.[/cyan] 🗑️ Eliminar multa")
        console.print(" [cyan]0.[/cyan] ↩ Volver")

        opcion = Prompt.ask(
            "\n[yellow]Seleccione una opción[/yellow]",
            choices=["0", "1", "2", "3", "4", "5"],
        )

        if opcion == "1":

            id_prestamo = obtener_uuid("ID del préstamo")

            if id_prestamo is None:
                pausar()
                continue

            prestamo = prestamo_crud.obtener_por_id(id_prestamo)

            if prestamo is None:

                mostrar_error("Préstamo no encontrado.")

                pausar()
                continue

            fecha_devolucion = None

            texto_devolucion = Prompt.ask(
                "Fecha de devolución (AAAA-MM-DD, vacío si no se ha devuelto)",
                default="",
            )

            if texto_devolucion.strip():

                try:

                    fecha_devolucion = datetime.strptime(
                        texto_devolucion, "%Y-%m-%d"
                    ).date()

                except ValueError:

                    mostrar_error("Fecha de devolución inválida.")

                    pausar()
                    continue

            estado = Prompt.ask("Estado", default="pendiente")

            multa = multa_crud.crear(
                id_prestamo=prestamo.id_prestamo,
                id_ejemplar=prestamo.id_ejemplar,
                fecha_prestamo=prestamo.fecha_prestamo,
                fecha_limite=prestamo.fecha_limite,
                fecha_devolucion=fecha_devolucion,
                estado=estado,
            )

            mostrar_exito("Multa creada correctamente.")

            console.print(Panel(str(multa), title="⚠️ Multa ", border_style="green"))

            pausar()

        elif opcion == "2":

            multas = multa_crud.obtener_todos()

            if not multas:

                console.print("[yellow]No hay multas registradas.[/yellow]")

            else:

                tabla = Table(show_lines=True)

                tabla.add_column("ID", style="cyan")
                tabla.add_column("Préstamo")
                tabla.add_column("Ejemplar")
                tabla.add_column("Préstamo")
                tabla.add_column("Límite")
                tabla.add_column("Devolución")
                tabla.add_column("Estado")

                for multa in multas:

                    tabla.add_row(
                        str(multa.id_multa),
                        str(multa.id_prestamo),
                        str(multa.id_ejemplar),
                        str(multa.fecha_prestamo),
                        str(multa.fecha_limite),
                        str(multa.fecha_devolucion),
                        multa.estado,
                    )

                console.print(tabla)

            pausar()

        elif opcion == "3":

            id_multa = obtener_uuid("ID de la multa")

            if id_multa:

                multa = multa_crud.obtener_por_id(id_multa)

                if multa is None:

                    mostrar_error("Multa no encontrada.")

                else:

                    console.print(
                        Panel(
                            str(multa), title="⚠️ Multa encontrada", border_style="blue"
                        )
                    )

            pausar()

        elif opcion == "4":

            id_multa = obtener_uuid("ID de la multa")

            if id_multa:

                multa = multa_crud.obtener_por_id(id_multa)

                if multa is None:

                    mostrar_error("Multa no encontrada.")

                else:

                    id_prestamo = obtener_uuid("ID del préstamo")

                    id_ejemplar = obtener_uuid("ID del ejemplar")

                    fecha_prestamo = obtener_fecha("Fecha del préstamo")

                    fecha_limite = obtener_fecha("Fecha límite")

                    if id_prestamo and id_ejemplar and fecha_prestamo and fecha_limite:

                        texto_devolucion = Prompt.ask(
                            "Fecha de devolución (AAAA-MM-DD, vacío si no se ha devuelto)",
                            default="",
                        )

                        fecha_devolucion = None

                        if texto_devolucion.strip():

                            try:

                                fecha_devolucion = datetime.strptime(
                                    texto_devolucion, "%Y-%m-%d"
                                ).date()

                            except ValueError:

                                mostrar_error("Fecha de devolución inválida.")

                                pausar()
                                continue

                        estado = Prompt.ask("Estado", default=multa.estado)

                        multa_crud.actualizar(
                            id_multa=id_multa,
                            id_prestamo=id_prestamo,
                            id_ejemplar=id_ejemplar,
                            fecha_prestamo=fecha_prestamo,
                            fecha_limite=fecha_limite,
                            fecha_devolucion=fecha_devolucion,
                            estado=estado,
                        )

                        mostrar_exito("Multa actualizada correctamente.")

            pausar()

        elif opcion == "5":

            id_multa = obtener_uuid("ID de la multa")

            if id_multa:

                multa = multa_crud.obtener_por_id(id_multa)

                if multa is None:

                    mostrar_error("Multa no encontrada.")

                else:

                    confirmar = Confirm.ask("¿Está seguro de eliminar esta multa?")

                    if confirmar:

                        if multa_crud.eliminar(id_multa):
                            mostrar_exito("Multa eliminada correctamente.")
                        else:
                            mostrar_error("No se pudo eliminar la multa.")

            pausar()

        elif opcion == "0":
            break


# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================


def main():

    usuario_crud = UsuarioCrud()
    libro_crud = LibroCrud()
    autor_crud = AutorCrud()
    categoria_crud = CategoriaCrud()
    editorial_crud = EditorialCrud()
    ejemplar_crud = EjemplarCrud()
    prestamo_crud = PrestamoCrud()
    multa_crud = MultaCrud()

    cargar_datos_prueba(
        usuario_crud,
        libro_crud,
        autor_crud,
        categoria_crud,
        editorial_crud,
        ejemplar_crud,
        prestamo_crud,
        multa_crud,
    )

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
            choices=[
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
            ],
        )

        if opcion == "1":

            menu_usuarios(usuario_crud)

        elif opcion == "2":
            menu_libros(libro_crud, categoria_crud, editorial_crud)

        elif opcion == "3":

            menu_autores(autor_crud)

        elif opcion == "4":

            menu_categorias(categoria_crud)

        elif opcion == "5":

            menu_editoriales(editorial_crud)

        elif opcion == "6":

            menu_ejemplares(ejemplar_crud, libro_crud)

        elif opcion == "7":

            menu_prestamos(prestamo_crud, usuario_crud)

        elif opcion == "8":

            menu_multas(multa_crud, prestamo_crud)

        elif opcion == "0":

            console.clear()

            console.print(
                Panel(
                    "[bold cyan]📚 Gracias por utilizar "
                    "la Biblioteca[/bold cyan]\n"
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
