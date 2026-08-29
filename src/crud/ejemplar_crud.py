import uuid
from datetime import date

from src.entities.ejemplar import Ejemplar


class EjemplarCrud:
    def __init__(self):
        self.ejemplares: list[Ejemplar] = []

    def crear(
        self,
        id_libro: uuid.UUID,
        codigo_inventario: str,
        fecha_adquisicion: date,
        estado: str,
        ubicacion: str,
    ) -> Ejemplar:
        ejemplar = Ejemplar(
            id_libro=id_libro,
            codigo_inventario=codigo_inventario,
            fecha_adquisicion=fecha_adquisicion,
            estado=estado,
            ubicacion=ubicacion,
        )

        self.ejemplares.append(ejemplar)
        return ejemplar

    def obtener_por_id(
        self,
        id_ejemplar: uuid.UUID,
    ) -> Ejemplar | None:
        for ejemplar in self.ejemplares:
            if ejemplar.id_ejemplar == id_ejemplar:
                return ejemplar

        return None

    def obtener_por_codigo_inventario(self, codigo_inventario: str) -> Ejemplar | None:
        codigo_normalizado = codigo_inventario.strip().lower()

        for ejemplar in self.ejemplares:
            if ejemplar.codigo_inventario.strip().lower() == codigo_normalizado:
                return ejemplar

        return None

    def obtener_todos(self) -> list[Ejemplar]:
        return self.ejemplares

    def actualizar(
        self,
        id_ejemplar: uuid.UUID,
        id_libro: uuid.UUID,
        codigo_inventario: str,
        fecha_adquisicion: date,
        estado: str,
        ubicacion: str,
    ) -> Ejemplar | None:
        ejemplar = self.obtener_por_id(id_ejemplar)

        if ejemplar is None:
            return None

        ejemplar.id_libro = id_libro
        ejemplar.codigo_inventario = codigo_inventario.strip()
        ejemplar.fecha_adquisicion = fecha_adquisicion
        ejemplar.estado = estado.strip()
        ejemplar.ubicacion = ubicacion.strip()

        return ejemplar

    def eliminar(self, id_ejemplar: uuid.UUID) -> bool:
        ejemplar = self.obtener_por_id(id_ejemplar)

        if ejemplar is None:
            return False

        self.ejemplares.remove(ejemplar)
        return True
