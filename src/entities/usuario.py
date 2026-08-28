import uuid
from datetime import date


class Usuario:
    def __init__(
        self,
        nombre: str,
        apellido: str,
        documento: str,
        correo: str,
        telefono: str,
        fecha_registro: date | None = None,
        estado: str = "activo",
        id_usuario: uuid.UUID | None = None,
    ):
        self.id_usuario = id_usuario if id_usuario is not None else uuid.uuid4()
        self.nombre = nombre.strip()
        self.apellido = apellido.strip()
        self.documento = documento.strip()
        self.correo = correo.strip()
        self.telefono = telefono.strip()
        self.fecha_registro = (
            fecha_registro if fecha_registro is not None else date.today()
        )
        self.estado = estado.strip()

    def __str__(self) -> str:
        return (
            f"ID: {self.id_usuario}\n"
            f"Nombre: {self.nombre}\n"
            f"Apellido: {self.apellido}\n"
            f"Documento: {self.documento}\n"
            f"Correo: {self.correo}\n"
            f"Teléfono: {self.telefono}\n"
            f"Fecha de registro: {self.fecha_registro}\n"
            f"Estado: {self.estado}"
        )
