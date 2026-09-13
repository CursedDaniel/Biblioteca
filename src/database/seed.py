import uuid
from datetime import date, timedelta

from src.database.database import Base, engine, SessionLocal

from src.entities.usuario import Usuario
from src.entities.autor import Autor
from src.entities.categoria import Categoria
from src.entities.editorial import Editorial
from src.entities.libro import Libro
from src.entities.ejemplar import Ejemplar
from src.entities.prestamo import Prestamo
from src.entities.multa import Multa

USUARIOS_SEED = [
    {
        "nombre": "Daniel",
        "apellido": "Londoño",
        "documento": "1001001001",
        "correo": "daniel@example.com",
        "telefono": "3001112233",
        "estado": "activo",
    },
    {
        "nombre": "Laura",
        "apellido": "Gómez",
        "documento": "1001001002",
        "correo": "laura@example.com",
        "telefono": "3002223344",
        "estado": "activo",
    },
    {
        "nombre": "Carlos",
        "apellido": "Martínez",
        "documento": "1001001003",
        "correo": "carlos@example.com",
        "telefono": "3003334455",
        "estado": "suspendido",
    },
]


AUTORES_SEED = [
    {
        "nombre": "Gabriel",
        "apellido": "García Márquez",
        "fecha_nacimiento": date(1927, 3, 6),
        "nacionalidad": "Colombiana",
        "biografia": "Escritor colombiano, autor de Cien años de soledad.",
    },
    {
        "nombre": "George",
        "apellido": "Orwell",
        "fecha_nacimiento": date(1903, 6, 25),
        "nacionalidad": "Británica",
        "biografia": "Escritor y periodista británico conocido por 1984 y Rebelión en la granja.",
    },
]


CATEGORIAS_SEED = [
    {
        "nombre": "Novela",
        "descripcion": "Obras literarias narrativas de ficción.",
    },
    {
        "nombre": "Ciencia ficción",
        "descripcion": "Obras relacionadas con ciencia, tecnología y futuros hipotéticos.",
    },
    {
        "nombre": "Fantasía",
        "descripcion": "Obras que incorporan elementos mágicos o sobrenaturales.",
    },
]


EDITORIALES_SEED = [
    {
        "nombre": "Editorial Planeta",
        "pais": "España",
        "ciudad": "Barcelona",
        "telefono": "934928000",
        "correo": "contacto@planeta.es",
    },
    {
        "nombre": "Penguin Random House",
        "pais": "Estados Unidos",
        "ciudad": "Nueva York",
        "telefono": "2127829000",
        "correo": "contacto@penguinrandomhouse.com",
    },
]


def seed_usuarios(session):
    usuarios = {}

    for datos in USUARIOS_SEED:
        existente = (
            session.query(Usuario).filter_by(documento=datos["documento"]).first()
        )

        if existente:
            usuarios[datos["documento"]] = existente
            print(f"  Usuario '{datos['nombre']} " f"{datos['apellido']}' ya existe.")
            continue

        usuario = Usuario(
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            documento=datos["documento"],
            correo=datos["correo"],
            telefono=datos["telefono"],
            fecha_registro=date.today(),
            estado=datos["estado"],
        )

        session.add(usuario)
        session.flush()

        usuarios[datos["documento"]] = usuario

        print(f"  Usuario '{datos['nombre']} " f"{datos['apellido']}' creado.")

    return usuarios


def seed_autores(session):
    autores = {}

    for datos in AUTORES_SEED:
        existente = (
            session.query(Autor)
            .filter_by(
                nombre=datos["nombre"],
                apellido=datos["apellido"],
            )
            .first()
        )

        if existente:
            autores[datos["apellido"]] = existente
            print(f"  Autor '{datos['nombre']} " f"{datos['apellido']}' ya existe.")
            continue

        autor = Autor(
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            fecha_nacimiento=datos["fecha_nacimiento"],
            nacionalidad=datos["nacionalidad"],
            biografia=datos["biografia"],
        )

        session.add(autor)
        session.flush()

        autores[datos["apellido"]] = autor

        print(f"  Autor '{datos['nombre']} " f"{datos['apellido']}' creado.")

    return autores


def seed_categorias(session):
    categorias = {}

    for datos in CATEGORIAS_SEED:
        existente = session.query(Categoria).filter_by(nombre=datos["nombre"]).first()

        if existente:
            categorias[datos["nombre"]] = existente
            print(f"  Categoría '{datos['nombre']}' ya existe.")
            continue

        categoria = Categoria(
            nombre=datos["nombre"],
            descripcion=datos["descripcion"],
        )

        session.add(categoria)
        session.flush()

        categorias[datos["nombre"]] = categoria

        print(f"  Categoría '{datos['nombre']}' creada.")

    return categorias


def seed_editoriales(session):
    editoriales = {}

    for datos in EDITORIALES_SEED:
        existente = session.query(Editorial).filter_by(nombre=datos["nombre"]).first()

        if existente:
            editoriales[datos["nombre"]] = existente
            print(f"  Editorial '{datos['nombre']}' ya existe.")
            continue

        editorial = Editorial(
            nombre=datos["nombre"],
            pais=datos["pais"],
            ciudad=datos["ciudad"],
            telefono=datos["telefono"],
            correo=datos["correo"],
        )

        session.add(editorial)
        session.flush()

        editoriales[datos["nombre"]] = editorial

        print(f"  Editorial '{datos['nombre']}' creada.")

    return editoriales


def seed_libros(session, categorias, editoriales, autores):
    libros = {}

    datos_libros = [
        {
            "titulo": "Cien años de soledad",
            "fecha_publicacion": date(1967, 5, 30),
            "numero_paginas": 417,
            "idiomas": "Español",
            "descripcion": "Novela sobre la familia Buendía y Macondo.",
            "categoria": "Novela",
            "editorial": "Editorial Planeta",
            "autor": "García Márquez",
        },
        {
            "titulo": "1984",
            "fecha_publicacion": date(1949, 6, 8),
            "numero_paginas": 328,
            "idiomas": "Español",
            "descripcion": "Novela distópica sobre una sociedad totalitaria.",
            "categoria": "Ciencia ficción",
            "editorial": "Penguin Random House",
            "autor": "Orwell",
        },
    ]

    for datos in datos_libros:
        existente = session.query(Libro).filter_by(titulo=datos["titulo"]).first()

        if existente:
            libros[datos["titulo"]] = existente
            print(f"  Libro '{datos['titulo']}' ya existe.")
            continue

        categoria = categorias[datos["categoria"]]
        editorial = editoriales[datos["editorial"]]
        autor = autores[datos["autor"]]

        libro = Libro(
            titulo=datos["titulo"],
            fecha_publicacion=datos["fecha_publicacion"],
            numero_paginas=datos["numero_paginas"],
            idiomas=datos["idiomas"],
            descripcion=datos["descripcion"],
            id_categoria=categoria.id_categoria,
            id_editorial=editorial.id_editorial,
        )

        libro.autores.append(autor)

        session.add(libro)
        session.flush()

        libros[datos["titulo"]] = libro

        print(f"  Libro '{datos['titulo']}' creado.")

    return libros


def seed_ejemplares(session, libros):
    ejemplares = {}

    datos_ejemplares = [
        {
            "codigo_inventario": "INV-0001",
            "fecha_adquisicion": date(2025, 1, 15),
            "estado": "disponible",
            "ubicacion": "Estante A1",
            "libro": "Cien años de soledad",
        },
        {
            "codigo_inventario": "INV-0002",
            "fecha_adquisicion": date(2025, 1, 16),
            "estado": "prestado",
            "ubicacion": "Estante A1",
            "libro": "1984",
        },
    ]

    for datos in datos_ejemplares:
        existente = (
            session.query(Ejemplar)
            .filter_by(codigo_inventario=datos["codigo_inventario"])
            .first()
        )

        if existente:
            ejemplares[datos["codigo_inventario"]] = existente
            print(f"  Ejemplar '{datos['codigo_inventario']}' ya existe.")
            continue

        libro = libros[datos["libro"]]

        ejemplar = Ejemplar(
            id_libro=libro.id_libro,
            codigo_inventario=datos["codigo_inventario"],
            fecha_adquisicion=datos["fecha_adquisicion"],
            estado=datos["estado"],
            ubicacion=datos["ubicacion"],
        )

        session.add(ejemplar)
        session.flush()

        ejemplares[datos["codigo_inventario"]] = ejemplar

        print(f"  Ejemplar '{datos['codigo_inventario']}' creado.")

    return ejemplares


def seed_prestamos(session, usuarios, ejemplares):
    prestamos = {}

    fecha_prestamo = date.today() - timedelta(days=5)
    fecha_limite = date.today() + timedelta(days=5)

    datos_prestamo = {
        "documento": "1001001002",
        "inventario": "INV-0002",
        "fecha_prestamo": fecha_prestamo,
        "fecha_limite": fecha_limite,
        "fecha_devolucion": None,
        "estado": "activo",
    }

    usuario = usuarios[datos_prestamo["documento"]]
    ejemplar = ejemplares[datos_prestamo["inventario"]]

    existente = (
        session.query(Prestamo)
        .filter_by(
            id_usuario=usuario.id_usuario,
            id_ejemplar=ejemplar.id_ejemplar,
        )
        .first()
    )

    if existente:
        prestamos["prestamo_1"] = existente
        print("  Préstamo ya existe.")
    else:
        prestamo = Prestamo(
            id_usuario=usuario.id_usuario,
            id_ejemplar=ejemplar.id_ejemplar,
            fecha_prestamo=datos_prestamo["fecha_prestamo"],
            fecha_limite=datos_prestamo["fecha_limite"],
            fecha_devolucion=datos_prestamo["fecha_devolucion"],
            estado=datos_prestamo["estado"],
        )

        session.add(prestamo)
        session.flush()

        prestamos["prestamo_1"] = prestamo

        print("  Préstamo creado.")

    return prestamos


def seed_multas(session, prestamos, ejemplares):
    prestamo = prestamos["prestamo_1"]
    ejemplar = ejemplares["INV-0002"]

    existente = session.query(Multa).filter_by(id_prestamo=prestamo.id_prestamo).first()

    if existente:
        print("  Multa ya existe.")
        return

    multa = Multa(
        fecha_prestamo=prestamo.fecha_prestamo,
        fecha_limite=prestamo.fecha_limite,
        fecha_devolucion=prestamo.fecha_devolucion,
        estado="pendiente",
        id_prestamo=prestamo.id_prestamo,
        id_ejemplar=ejemplar.id_ejemplar,
    )

    session.add(multa)
    session.flush()

    print("  Multa creada.")


def seed():
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        print("\nSembrando usuarios...")
        usuarios = seed_usuarios(session)

        print("\nSembrando autores...")
        autores = seed_autores(session)

        print("\nSembrando categorías...")
        categorias = seed_categorias(session)

        print("\nSembrando editoriales...")
        editoriales = seed_editoriales(session)

        print("\nSembrando libros...")
        libros = seed_libros(
            session,
            categorias,
            editoriales,
            autores,
        )

        print("\nSembrando ejemplares...")
        ejemplares = seed_ejemplares(
            session,
            libros,
        )

        print("\nSembrando préstamos...")
        prestamos = seed_prestamos(
            session,
            usuarios,
            ejemplares,
        )

        print("\nSembrando multas...")
        seed_multas(
            session,
            prestamos,
            ejemplares,
        )

        session.commit()

        print("\nSeeder completado correctamente.")

    except Exception:
        session.rollback()
        print("\nError en el seeder. Se revirtió la transacción.")
        raise

    finally:
        session.close()


if __name__ == "__main__":
    seed()