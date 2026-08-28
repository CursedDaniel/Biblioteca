import uuid
from datetime import date


class Ejemplar:
    def __init__(
        self,
        id_libro: uuid.UUID,
        codigo_inventario: str,
        fecha_adquisicion: date,
        estado: str,
        ubicacion: str,
        id_ejemplar: uuid.UUID | None = None,
    ):
        self.id_ejemplar = id_ejemplar if id_ejemplar is not None else uuid.uuid4()
        self.id_libro = id_libro
        self.codigo_inventario = codigo_inventario.strip()
        self.fecha_adquisicion = (
            (fecha_adquisicion is not None) and fecha_adquisicion or date.today()
        )
        self.estado = estado.strip()
        self.ubicacion = ubicacion.strip()

    def __str__(self) -> str:
        return (
            f"ID: {self.id_ejemplar}\n"
            f"ID Libro: {self.id_libro}\n"
            f"Código de Inventario: {self.codigo_inventario}\n"
            f"Fecha de Adquisición: {self.fecha_adquisicion}\n"
            f"Estado: {self.estado}\n"
            f"Ubicación: {self.ubicacion}"
        )
