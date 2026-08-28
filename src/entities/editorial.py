import uuid
from datetime import date


class Editorial:
    def __init__(
        self,
        nombre: str,
        pais: str,
        ciudad: str,
        correo: str,
        telefono: str,
        id_editorial: uuid.UUID | None = None,
    ):
        self.id_editorial = id_editorial if id_editorial is not None else uuid.uuid4()
        self.nombre = nombre.strip()
        self.pais = pais.strip()
        self.ciudad = ciudad.strip()
        self.correo = correo.strip()
        self.telefono = telefono.strip()

    def __str__(self) -> str:
        return (
            f"ID: {self.id_editorial}\n"
            f"Nombre: {self.nombre}\n"
            f"País: {self.pais}\n"
            f"Ciudad: {self.ciudad}\n"
            f"Correo: {self.correo}\n"
            f"Teléfono: {self.telefono}"
        )
