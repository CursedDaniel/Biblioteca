class Libro:
    def __init__(
        self,
        id_libro: int,
        titulo: str,
        fecha_publicacion: str,
        numero_paginas: str,
        idioma: str,
        descripcion: str,
        id_categoria: str,
        id_editorial: str,
    ):
        self.id_libro = id_libro
        self.titulo = titulo
        self.fecha_publicacion = fecha_publicacion
        self.numero_paginas = numero_paginas
        self.idioma = idioma
        self.descripcion = descripcion
        self.id_categoria = id_categoria
        self.id_editorial = id_editorial
