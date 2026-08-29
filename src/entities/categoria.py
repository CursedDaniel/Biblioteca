import uuid


class Categoria:
    def __init__(
        self,
        nombre: str,
        descripcion: str,
        id_categoria: uuid.UUID | None = None,
    ):
        self.id_categoria = (
            id_categoria if id_categoria is not None else uuid.uuid4()
        )
        self.nombre = nombre.strip()
        self.descripcion = descripcion.strip()

    def __str__(self) -> str:
        return (
            f"ID: {self.id_categoria}\n"
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}"
        )