
import random
from datetime import date, timedelta


def cargar_datos_prueba(
    usuario_crud,
    libro_crud,
    autor_crud,
    categoria_crud,
    editorial_crud,
    ejemplar_crud,
    prestamo_crud,
    multa_crud,
):
    """
    Carga datos temporales de prueba en todos los CRUD.
    Los datos se generan automáticamente al iniciar el programa.
    """

    # ==========================================================
    # CATEGORÍAS
    # ==========================================================

    categorias = [
        categoria_crud.crear(
            nombre="Ciencia Ficción",
            descripcion="Libros relacionados con ciencia ficción y futuros posibles.",
        ),
        categoria_crud.crear(
            nombre="Aventura",
            descripcion="Historias de aventura, acción y exploración.",
        ),
        categoria_crud.crear(
            nombre="Historia",
            descripcion="Libros relacionados con acontecimientos históricos.",
        ),
        categoria_crud.crear(
            nombre="Fantasía",
            descripcion="Historias de mundos fantásticos y magia.",
        ),
    ]

    # ==========================================================
    # EDITORIALES
    # ==========================================================

    editoriales = [
        editorial_crud.crear(
            nombre="Planeta",
            pais="España",
            ciudad="Barcelona",
            telefono="934876500",
            correo="contacto@planeta.com",
        ),
        editorial_crud.crear(
            nombre="Penguin Random House",
            pais="Estados Unidos",
            ciudad="Nueva York",
            telefono="2127829000",
            correo="contacto@penguin.com",
        ),
        editorial_crud.crear(
            nombre="HarperCollins",
            pais="Estados Unidos",
            ciudad="Nueva York",
            telefono="2122077000",
            correo="contacto@harpercollins.com",
        ),
    ]

    # ==========================================================
    # AUTORES
    # ==========================================================

    autores = [
        autor_crud.crear(
            nombre="Gabriel",
            apellido="García Márquez",
            fecha_nacimiento=date(1927, 3, 6),
            nacionalidad="Colombiana",
            biografia="Escritor colombiano reconocido mundialmente.",
        ),
        autor_crud.crear(
            nombre="J. R. R.",
            apellido="Tolkien",
            fecha_nacimiento=date(1892, 1, 3),
            nacionalidad="Británica",
            biografia="Escritor británico conocido por sus obras de fantasía.",
        ),
        autor_crud.crear(
            nombre="Isaac",
            apellido="Asimov",
            fecha_nacimiento=date(1920, 1, 2),
            nacionalidad="Estadounidense",
            biografia="Escritor y divulgador científico especializado en ciencia ficción.",
        ),
        autor_crud.crear(
            nombre="Julio",
            apellido="Verne",
            fecha_nacimiento=date(1828, 2, 8),
            nacionalidad="Francesa",
            biografia="Escritor francés considerado uno de los padres de la ciencia ficción.",
        ),
    ]

    # ==========================================================
    # LIBROS
    # ==========================================================

    libros = [
        libro_crud.crear(
            titulo="Cien años de soledad",
            fecha_publicacion=date(1967, 5, 30),
            numero_paginas=471,
            idiomas="Español",
            descripcion="Novela clásica de la literatura latinoamericana.",
            id_categoria=categorias[2].id_categoria,
            id_editorial=editoriales[0].id_editorial,
        ),
        libro_crud.crear(
            titulo="El señor de los anillos",
            fecha_publicacion=date(1954, 7, 29),
            numero_paginas=1178,
            idiomas="Español, Inglés",
            descripcion="Historia épica ambientada en la Tierra Media.",
            id_categoria=categorias[3].id_categoria,
            id_editorial=editoriales[1].id_editorial,
        ),
        libro_crud.crear(
            titulo="Fundación",
            fecha_publicacion=date(1951, 5, 1),
            numero_paginas=255,
            idiomas="Inglés, Español",
            descripcion="Obra clásica de ciencia ficción.",
            id_categoria=categorias[0].id_categoria,
            id_editorial=editoriales[2].id_editorial,
        ),
        libro_crud.crear(
            titulo="Viaje al centro de la Tierra",
            fecha_publicacion=date(1864, 11, 25),
            numero_paginas=384,
            idiomas="Francés, Español",
            descripcion="Novela de aventuras y exploración.",
            id_categoria=categorias[1].id_categoria,
            id_editorial=editoriales[0].id_editorial,
        ),
        libro_crud.crear(
            titulo="Rambo",
            fecha_publicacion=date(1985, 5, 31),
            numero_paginas=655,
            idiomas="Inglés",
            descripcion="Novela de acción y aventura.",
            id_categoria=categorias[1].id_categoria,
            id_editorial=editoriales[1].id_editorial,
        ),
    ]

    # ==========================================================
    # EJEMPLARES
    # ==========================================================

    ejemplares = []

    contador = 1

    for libro in libros:
        cantidad = random.randint(1, 3)

        for _ in range(cantidad):
            ejemplar = ejemplar_crud.crear(
                id_libro=libro.id_libro,
                codigo_inventario=f"INV-{contador:04d}",
                fecha_adquisicion=date.today()
                - timedelta(days=random.randint(30, 1500)),
                estado=random.choice(
                    ["Disponible", "Disponible", "Disponible", "Prestado"]
                ),
                ubicacion=random.choice(
                    [
                        "Estante A1",
                        "Estante A2",
                        "Estante B1",
                        "Estante B2",
                        "Estante C1",
                    ]
                ),
            )

            ejemplares.append(ejemplar)
            contador += 1

    # ==========================================================
    # USUARIOS
    # ==========================================================

    usuarios = [
        usuario_crud.crear(
            nombre="Daniel",
            apellido="Londoño",
            documento="1001001001",
            correo="daniel@example.com",
            telefono="3001112233",
            fecha_registro=date.today() - timedelta(days=300),
            estado="activo",
        ),
        usuario_crud.crear(
            nombre="Laura",
            apellido="Gómez",
            documento="1001001002",
            correo="laura@example.com",
            telefono="3012223344",
            fecha_registro=date.today() - timedelta(days=250),
            estado="activo",
        ),
        usuario_crud.crear(
            nombre="Carlos",
            apellido="Martínez",
            documento="1001001003",
            correo="carlos@example.com",
            telefono="3023334455",
            fecha_registro=date.today() - timedelta(days=180),
            estado="activo",
        ),
        usuario_crud.crear(
            nombre="Sofía",
            apellido="Ramírez",
            documento="1001001004",
            correo="sofia@example.com",
            telefono="3034445566",
            fecha_registro=date.today() - timedelta(days=100),
            estado="activo",
        ),
        usuario_crud.crear(
            nombre="Andrés",
            apellido="Torres",
            documento="1001001005",
            correo="andres@example.com",
            telefono="3045556677",
            fecha_registro=date.today() - timedelta(days=50),
            estado="suspendido",
        ),
    ]

    # ==========================================================
    # PRÉSTAMOS
    # ==========================================================

    prestamos = []

    ejemplares_disponibles = [
        ejemplar
        for ejemplar in ejemplares
        if ejemplar.estado.lower() == "disponible"
    ]

    cantidad_prestamos = min(4, len(ejemplares_disponibles))

    for i in range(cantidad_prestamos):
        ejemplar = ejemplares_disponibles[i]
        usuario = usuarios[i % len(usuarios)]

        fecha_prestamo = date.today() - timedelta(
            days=random.randint(1, 30)
        )

        fecha_limite = fecha_prestamo + timedelta(days=15)

        # Algunos préstamos ya fueron devueltos
        if i % 2 == 0:
            fecha_devolucion = fecha_prestamo + timedelta(
                days=random.randint(5, 14)
            )
            estado = "devuelto"
        else:
            fecha_devolucion = None
            estado = "activo"

        prestamo = prestamo_crud.crear(
            id_usuario=usuario.id_usuario,
            id_ejemplar=ejemplar.id_ejemplar,
            fecha_prestamo=fecha_prestamo,
            fecha_limite=fecha_limite,
            fecha_devolucion=fecha_devolucion,
            estado=estado,
        )

        prestamos.append(prestamo)

    # ==========================================================
    # MULTAS
    # ==========================================================

    # Solo creamos multas si existen préstamos
    for prestamo in prestamos:
        # Una multa aleatoria para algunos préstamos
        if prestamo.estado.lower() != "devuelto" and date.today() > prestamo.fecha_limite:
            multa_crud.crear(
                id_prestamo=prestamo.id_prestamo,
                id_ejemplar=prestamo.id_ejemplar,
                fecha_prestamo=prestamo.fecha_prestamo,
                fecha_limite=prestamo.fecha_limite,
                fecha_devolucion=prestamo.fecha_devolucion,
                estado="pendiente",
            )

    print("Datos de prueba cargados correctamente.")

