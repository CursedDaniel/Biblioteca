from datetime import date


class Ejemplar:
    def __init__(
        self,
        id_ejemplar: int,
        id_libro: int,
        codigo_inventario: str,
        fecha_adquisicion: date,
        estado: str,
        ubicacion: str,
    ):
        self.id_ejemplar = id_ejemplar
        self.id_libro = id_libro
        self.codigo_inventario = codigo_inventario
        self.fecha_adquisicion = fecha_adquisicion
        self.estado = estado
        self.ubicacion = ubicacion
