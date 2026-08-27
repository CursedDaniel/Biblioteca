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
        self.fecha_adquisicion = fecha_adquisicion
        self.estado = estado.strip()
        self.ubicacion = ubicacion.strip()
