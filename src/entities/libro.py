import uuid
from datetime import date


class Libro:
    def __init__(
        self,
        titulo: str,
        fecha_publicacion: date,
        numero_paginas: str,
        idiomas: str,
        descripcion: str,
        id_categoria: str,
        id_editorial: str,
        id_libro: uuid.UUID | None = None,
    ):
        self.id_libro = id_libro if id_libro is not None else uuid.uuid4()
        self.titulo = titulo
        self.fecha_publicacion = fecha_publicacion
        self.numero_paginas = numero_paginas
        self.idiomas = idiomas
        self.descripcion = descripcion
        self.id_categoria = id_categoria
        self.id_editorial = id_editorial

    def __str__(self) -> str:
        return (
            f"ID: {self.id_libro}\n"
            f"Título: {self.titulo}\n"
            f"Fecha de Publicación: {self.fecha_publicacion}\n"
            f"Número de Páginas: {self.numero_paginas}\n"
            f"Idiomas: {self.idiomas}\n"
            f"Descripción: {self.descripcion}\n"
            f"ID Categoría: {self.id_categoria}\n"
            f"ID Editorial: {self.id_editorial}"
        )
