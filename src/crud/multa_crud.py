import uuid
from datetime import date

from src.entities.multa import Multa


class MultaCrud:
    def __init__(self):
        self.multas: list[Multa] = []

    def crear(
        self,
        id_prestamo: uuid.UUID,
        id_ejemplar: uuid.UUID,
        fecha_prestamo: date,
        fecha_limite: date,
        fecha_devolucion: date | None = None,
        estado: str = "pendiente",
    ) -> Multa:
        multa = Multa(
            id_prestamo=id_prestamo,
            id_ejemplar=id_ejemplar,
            fecha_prestamo=fecha_prestamo,
            fecha_limite=fecha_limite,
            fecha_devolucion=fecha_devolucion,
            estado=estado,
        )

        self.multas.append(multa)
        return multa

    def obtener_por_id(
        self,
        id_multa: uuid.UUID,
    ) -> Multa | None:
        for multa in self.multas:
            if multa.id_multa == id_multa:
                return multa

        return None

    def obtener_todos(self) -> list[Multa]:
        return self.multas

    def actualizar(
        self,
        id_multa: uuid.UUID,
        id_prestamo: uuid.UUID,
        id_ejemplar: uuid.UUID,
        fecha_prestamo: date,
        fecha_limite: date,
        fecha_devolucion: date | None,
        estado: str,
    ) -> Multa | None:
        multa = self.obtener_por_id(id_multa)

        if multa is None:
            return None

        multa.id_prestamo = id_prestamo
        multa.id_ejemplar = id_ejemplar
        multa.fecha_prestamo = fecha_prestamo
        multa.fecha_limite = fecha_limite
        multa.fecha_devolucion = fecha_devolucion
        multa.estado = estado.strip()

        return multa

    def eliminar(self, id_multa: uuid.UUID) -> bool:
        multa = self.obtener_por_id(id_multa)

        if multa is None:
            return False

        self.multas.remove(multa)
        return True
