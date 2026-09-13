import uuid
from datetime import date

from sqlalchemy.orm import Session

from src.entities.libro import Libro


class LibroCrud:
    def crear(
        self,
        session: Session,
        titulo: str,
        fecha_publicacion: date,
        numero_paginas: int,
        idiomas: str,
        descripcion: str,
        id_categoria: uuid.UUID,
        id_editorial: uuid.UUID,
    ) -> Libro:

        libro = Libro(
            titulo=titulo,
            fecha_publicacion=fecha_publicacion,
            numero_paginas=numero_paginas,
            idiomas=idiomas,
            descripcion=descripcion,
            id_categoria=id_categoria,
            id_editorial=id_editorial,
        )

        session.add(libro)
        session.commit()
        session.refresh(libro)

        return libro

    def obtener_por_id(
        self,
        session: Session,
        id_libro: uuid.UUID,
    ) -> Libro | None:

        return session.get(Libro, id_libro)

    def obtener_por_titulo(
        self,
        session: Session,
        titulo: str,
    ) -> Libro | None:

        titulo_normalizado = titulo.strip().lower()

        libros = session.query(Libro).all()

        for libro in libros:
            if libro.titulo.strip().lower() == titulo_normalizado:
                return libro

        return None

    def obtener_todos(
        self,
        session: Session,
    ) -> list[Libro]:

        return session.query(Libro).all()

    def actualizar(
        self,
        session: Session,
        id_libro: uuid.UUID,
        titulo: str,
        fecha_publicacion: date,
        numero_paginas: int,
        idiomas: str,
        descripcion: str,
        id_categoria: uuid.UUID,
        id_editorial: uuid.UUID,
    ) -> Libro | None:

        libro = self.obtener_por_id(session, id_libro)

        if libro is None:
            return None

        libro.titulo = titulo.strip()
        libro.fecha_publicacion = fecha_publicacion
        libro.numero_paginas = numero_paginas
        libro.idiomas = idiomas.strip()
        libro.descripcion = descripcion.strip()
        libro.id_categoria = id_categoria
        libro.id_editorial = id_editorial

        session.commit()
        session.refresh(libro)

        return libro

    def eliminar(
        self,
        session: Session,
        id_libro: uuid.UUID,
    ) -> bool:

        libro = self.obtener_por_id(session, id_libro)

        if libro is None:
            return False

        session.delete(libro)
        session.commit()

        return True
