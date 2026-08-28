import uuid
from datetime import date


class Prestamo:
    def __init__(
        self,
        id_usuario: uuid.UUID,
        id_ejemplar: uuid.UUID,
        fecha_prestamo: date,
        fecha_limite: date,
        fecha_devolucion: date | None = None,
        estado: str = "activo",
        id_prestamo: uuid.UUID | None = None,
    ):
        self.id_prestamo = id_prestamo if id_prestamo is not None else uuid.uuid4()
        self.id_usuario = id_usuario
        self.id_ejemplar = id_ejemplar
        self.fecha_prestamo = fecha_prestamo
        self.fecha_limite = fecha_limite
        self.fecha_devolucion = fecha_devolucion
        self.estado = estado.strip()

    def __str__(self) -> str:
        return (
            f"ID: {self.id_prestamo}\n"
            f"Usuario: {self.id_usuario}\n"
            f"Ejemplar: {self.id_ejemplar}\n"
            f"Fecha de préstamo: {self.fecha_prestamo}\n"
            f"Fecha límite: {self.fecha_limite}\n"
            f"Fecha de devolución: {self.fecha_devolucion}\n"
            f"Estado: {self.estado}"
        )
