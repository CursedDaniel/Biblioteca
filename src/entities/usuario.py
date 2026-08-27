import uuid
from datetime import date


class Usuario:
    def __init__(
        self,
        id_usuario: uuid.UUID | None,
        nombre: str,
        apellido: str,
        documento: str,
        correo: str,
        telefono: str,
        fecha_registro: date,
        estado: str,
    ):
        self.id_usuario = id_usuario if id_usuario is not None else uuid.uuid4()
        self.nombre = nombre.strip()
        self.apellido = apellido.strip()
        self.documento = documento.strip()
        self.correo = correo.strip()
        self.telefono = telefono.strip()
        self.fecha_registro = fecha_registro
        self.estado = estado.strip()

    def nombre_completo(self) -> str:
        partes = [self.nombre, self.apellido]
        return " ".join(parte for parte in partes if parte).strip()

    def __str__(self) -> str:
        return (
            f"ID: {self.id_usuario}\n"
            f"Nombre: {self.nombre_completo()}\n"
            f"Usuario: {self.nombre_usuario}"
        )
