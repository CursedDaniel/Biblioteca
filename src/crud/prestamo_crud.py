import uuid
from datetime import date

from sqlalchemy.orm import Session

from src.entities.prestamo import Prestamo


class PrestamoCrud:
    def __init__(self, session: Session):
        self.session = session

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
            estado=estado.strip(),
        )

        self.session.add(prestamo)
        self.session.commit()
        self.session.refresh(prestamo)

        return prestamo

    def obtener_por_id(self, id_prestamo: uuid.UUID) -> Prestamo | None:
        return self.session.get(Prestamo, id_prestamo)

    def obtener_todos(self) -> list[Prestamo]:
        return self.session.query(Prestamo).all()

    def obtener_por_usuario_y_ejemplar(
        self,
        id_usuario: uuid.UUID,
        id_ejemplar: uuid.UUID,
    ) -> list[Prestamo]:
        return (
            self.session.query(Prestamo)
            .filter(
                Prestamo.id_usuario == id_usuario,
                Prestamo.id_ejemplar == id_ejemplar,
            )
            .all()
        )

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

        self.session.commit()
        self.session.refresh(prestamo)

        return prestamo

    def eliminar(self, id_prestamo: uuid.UUID) -> bool:
        prestamo = self.obtener_por_id(id_prestamo)

        if prestamo is None:
            return False

        self.session.delete(prestamo)
        self.session.commit()

        return True
        
