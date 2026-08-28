import uuid
from datetime import date

class Multa:
    def __init__(
        self,
        fecha_prestamo: date,
        fecha_limite: date,
        fecha_devolucion: date,
        estado: str,
        id_multa: uuid.UUID | None = None,
        id_prestamo: uuid.UUID | None = None,
    ):
        self.id_multa = id_multa if id_multa is not None else uuid.uuid4()
        self.fecha_prestamo = fecha_prestamo
        self.fecha_limite = fecha_limite
        self.fecha_devolucion = fecha_devolucion
        self.estado = estado.strip()
        self.id_prestamo = id_prestamo if id_prestamo is not None else uuid.uuid4()
        
    def __str__(self) -> str:
        return (
            f"ID: {self.id_multa}\n"
            f"Fecha de Préstamo: {self.fecha_prestamo}\n"
            f"Fecha Límite: {self.fecha_limite}\n"
            f"Fecha de Devolución: {self.fecha_devolucion}\n"
            f"Estado: {self.estado}\n"
            f"ID del Préstamo: {self.id_prestamo}"
        )
        