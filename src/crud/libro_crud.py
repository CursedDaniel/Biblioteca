import uuid
from datetime import date

from sqlalchemy.orm import Session

from src.entities.libro import Libro


class LibroCrud:
    def __init__(self, session: Session):
        self.session = session

    def crear(
        self,
        titulo: str,
        fecha_publicacion: date,
        numero_paginas: int,
        idiomas: str,
        descripcion: str,
        id_categoria: uuid.UUID,
        id_editorial: uuid.UUID,
    ) -> Libro:
        libro = Libro(
            titulo=titulo.strip(),
            fecha_publicacion=fecha_publicacion,
            numero_paginas=numero_paginas,
            idiomas=idiomas.strip(),
            descripcion=descripcion.strip(),
            id_categoria=id_categoria,
            id_editorial=id_editorial,
        )

        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)

        return libro

    def obtener_por_id(self, id_libro: uuid.UUID) -> Libro | None:
        return self.session.get(Libro, id_libro)

    def obtener_por_titulo(self, titulo: str) -> Libro | None:
        titulo_normalizado = titulo.strip()

        return (
            self.session.query(Libro)
            .filter(Libro.titulo.ilike(titulo_normalizado))
            .first()
        )

    def obtener_todos(self) -> list[Libro]:
        return self.session.query(Libro).all()

    def actualizar(
        self,
        id_libro: uuid.UUID,
        titulo: str,
        fecha_publicacion: date,
        numero_paginas: int,
        idiomas: str,
        descripcion: str,
        id_categoria: uuid.UUID,
        id_editorial: uuid.UUID,
    ) -> Libro | None:
        libro = self.obtener_por_id(id_libro)

        if libro is None:
            return None

        libro.titulo = titulo.strip()
        libro.fecha_publicacion = fecha_publicacion
        libro.numero_paginas = numero_paginas
        libro.idiomas = idiomas.strip()
        libro.descripcion = descripcion.strip()
        libro.id_categoria = id_categoria
        libro.id_editorial = id_editorial

        self.session.commit()
        self.session.refresh(libro)

        return libro

    def eliminar(self, id_libro: uuid.UUID) -> bool:
        libro = self.obtener_por_id(id_libro)

        if libro is None:
            return False

        self.session.delete(libro)
        self.session.commit()

        return True
