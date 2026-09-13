import uuid
from datetime import date

from sqlalchemy.orm import Session

from src.entities.prestamo import Prestamo


class PrestamoCrud:
    def crear(
        self,
        session: Session,
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

        session.add(prestamo)
        session.commit()
        session.refresh(prestamo)

        return prestamo

    def obtener_por_id(
        self,
        session: Session,
        id_prestamo: uuid.UUID,
    ) -> Prestamo | None:

        return session.get(Prestamo, id_prestamo)

    def obtener_todos(
        self,
        session: Session,
    ) -> list[Prestamo]:

        return session.query(Prestamo).all()

    def obtener_por_usuario_y_ejemplar(
        self,
        session: Session,
        id_usuario: uuid.UUID,
        id_ejemplar: uuid.UUID,
    ) -> list[Prestamo]:

        return (
            session.query(Prestamo)
            .filter(
                Prestamo.id_usuario == id_usuario,
                Prestamo.id_ejemplar == id_ejemplar,
            )
            .all()
        )

    def actualizar(
        self,
        session: Session,
        id_prestamo: uuid.UUID,
        id_usuario: uuid.UUID,
        id_ejemplar: uuid.UUID,
        fecha_prestamo: date,
        fecha_limite: date,
        fecha_devolucion: date | None,
        estado: str,
    ) -> Prestamo | None:

        prestamo = self.obtener_por_id(session, id_prestamo)

        if prestamo is None:
            return None

        prestamo.id_usuario = id_usuario
        prestamo.id_ejemplar = id_ejemplar
        prestamo.fecha_prestamo = fecha_prestamo
        prestamo.fecha_limite = fecha_limite
        prestamo.fecha_devolucion = fecha_devolucion
        prestamo.estado = estado.strip()

        session.commit()
        session.refresh(prestamo)

        return prestamo

    def eliminar(
        self,
        session: Session,
        id_prestamo: uuid.UUID,
    ) -> bool:

        prestamo = self.obtener_por_id(session, id_prestamo)

        if prestamo is None:
            return False

        session.delete(prestamo)
        session.commit()

        return True
        
