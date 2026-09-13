import uuid
from datetime import date

from sqlalchemy.orm import Session

from src.entities.multa import Multa


class MultaCrud:
    def crear(
        self,
        session: Session,
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

        session.add(multa)
        session.commit()
        session.refresh(multa)

        return multa

    def obtener_por_id(
        self,
        session: Session,
        id_multa: uuid.UUID,
    ) -> Multa | None:

        return session.get(Multa, id_multa)

    def obtener_todos(
        self,
        session: Session,
    ) -> list[Multa]:

        return session.query(Multa).all()

    def actualizar(
        self,
        session: Session,
        id_multa: uuid.UUID,
        id_prestamo: uuid.UUID,
        id_ejemplar: uuid.UUID,
        fecha_prestamo: date,
        fecha_limite: date,
        fecha_devolucion: date | None,
        estado: str,
    ) -> Multa | None:

        multa = self.obtener_por_id(session, id_multa)

        if multa is None:
            return None

        multa.id_prestamo = id_prestamo
        multa.id_ejemplar = id_ejemplar
        multa.fecha_prestamo = fecha_prestamo
        multa.fecha_limite = fecha_limite
        multa.fecha_devolucion = fecha_devolucion
        multa.estado = estado.strip()

        session.commit()
        session.refresh(multa)

        return multa

    def eliminar(
        self,
        session: Session,
        id_multa: uuid.UUID,
    ) -> bool:

        multa = self.obtener_por_id(session, id_multa)

        if multa is None:
            return False

        session.delete(multa)
        session.commit()

        return True
