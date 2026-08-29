import uuid
from datetime import date

from src.entities.prestamo import Prestamo


class PrestamoCrud:
    def __init__(self):
        self.prestamos: list[Prestamo] = []

    def crear(
        self,
        id_usuario: uuid.UUID,
        id_ejemplar: uuid.UUID,
        fecha_prestamo: date,
        fecha_limite: date,
        fecha_devolucion: date | None = None,
        estado: str = "activo",
    ) -> Prestamo:
        prestamo = Prestamo(
            id_usuario=id_usuario,
            id_ejemplar=id_ejemplar,
            fecha_prestamo=fecha_prestamo,
            fecha_limite=fecha_limite,
            fecha_devolucion=fecha_devolucion,
            estado=estado,
        )

        self.prestamos.append(prestamo)
        return prestamo

    def obtener_por_id(
        self,
        id_prestamo: uuid.UUID,
    ) -> Prestamo | None:
        for prestamo in self.prestamos:
            if prestamo.id_prestamo == id_prestamo:
                return prestamo

        return None

    def obtener_todos(self) -> list[Prestamo]:
        return self.prestamos

    def obtener_por_usuario_y_ejemplar(
        self,
        id_usuario: uuid.UUID,
        id_ejemplar: uuid.UUID,
    ) -> list[Prestamo]:
        return [
            prestamo
            for prestamo in self.prestamos
            if prestamo.id_usuario == id_usuario and prestamo.id_ejemplar == id_ejemplar
        ]

    def actualizar(
        self,
        id_prestamo: uuid.UUID,
        id_usuario: uuid.UUID,
        id_ejemplar: uuid.UUID,
        fecha_prestamo: date,
        fecha_limite: date,
        fecha_devolucion: date | None,
        estado: str,
    ) -> Prestamo | None:
        prestamo = self.obtener_por_id(id_prestamo)

        if prestamo is None:
            return None

        prestamo.id_usuario = id_usuario
        prestamo.id_ejemplar = id_ejemplar
        prestamo.fecha_prestamo = fecha_prestamo
        prestamo.fecha_limite = fecha_limite
        prestamo.fecha_devolucion = fecha_devolucion
        prestamo.estado = estado.strip()

        return prestamo

    def eliminar(self, id_prestamo: uuid.UUID) -> bool:
        prestamo = self.obtener_por_id(id_prestamo)

        if prestamo is None:
            return False

        self.prestamos.remove(prestamo)
        return True
