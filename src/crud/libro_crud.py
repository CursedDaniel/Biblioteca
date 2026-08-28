import uuid
from datetime import date

from src.entities.libro import Libro


class LibroCrud:
    def __init__(self):
        self.libros: list[Libro] = []

    def crear(
        self,
        titulo: str,
        fecha_publicacion: date,
        numero_paginas: int,
        idioma: str,
        descripcion: str,
        id_categoria: uuid.UUID,
        id_editorial: uuid.UUID,
    ) -> Libro:
        libro = Libro(
            titulo=titulo,
            fecha_publicacion=fecha_publicacion,
            numero_paginas=numero_paginas,
            idioma=idioma,
            descripcion=descripcion,
            id_categoria=id_categoria,
            id_editorial=id_editorial,
        )

        self.libros.append(libro)
        return libro

    def obtener_por_id(
        self,
        id_libro: uuid.UUID,
    ) -> Libro | None:
        for libro in self.libros:
            if libro.id_libro == id_libro:
                return libro

        return None

    def obtener_todos(self) -> list[Libro]:
        return self.libros

    def actualizar(
        self,
        id_libro: uuid.UUID,
        titulo: str,
        fecha_publicacion: date,
        numero_paginas: int,
        idioma: str,
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
        libro.idioma = idioma.strip()
        libro.descripcion = descripcion.strip()
        libro.id_categoria = id_categoria
        libro.id_editorial = id_editorial

        return libro

    def eliminar(self, id_libro: uuid.UUID) -> bool:
        libro = self.obtener_por_id(id_libro)

        if libro is None:
            return False

        self.libros.remove(libro)
        return True
