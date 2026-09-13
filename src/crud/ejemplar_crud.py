import uuid
from datetime import date

from sqlalchemy.orm import Session

from src.entities.ejemplar import Ejemplar


class EjemplarCrud:
    def crear(
        self,
        session: Session,
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

        session.add(ejemplar)
        session.commit()
        session.refresh(ejemplar)

        return ejemplar

    def obtener_por_id(
        self,
        session: Session,
        id_ejemplar: uuid.UUID,
    ) -> Ejemplar | None:

        return session.get(Ejemplar, id_ejemplar)

    def obtener_por_codigo_inventario(
        self,
        session: Session,
        codigo_inventario: str,
    ) -> Ejemplar | None:

        codigo_normalizado = codigo_inventario.strip().lower()

        ejemplares = session.query(Ejemplar).all()

        for ejemplar in ejemplares:
            if (
                ejemplar.codigo_inventario.strip().lower()
                == codigo_normalizado
            ):
                return ejemplar

        return None

    def obtener_todos(
        self,
        session: Session,
    ) -> list[Ejemplar]:

        return session.query(Ejemplar).all()

    def actualizar(
        self,
        session: Session,
        id_ejemplar: uuid.UUID,
        id_libro: uuid.UUID,
        codigo_inventario: str,
        fecha_adquisicion: date,
        estado: str,
        ubicacion: str,
    ) -> Ejemplar | None:

        ejemplar = self.obtener_por_id(session, id_ejemplar)

        if ejemplar is None:
            return None

        ejemplar.id_libro = id_libro
        ejemplar.codigo_inventario = codigo_inventario.strip()
        ejemplar.fecha_adquisicion = fecha_adquisicion
        ejemplar.estado = estado.strip()
        ejemplar.ubicacion = ubicacion.strip()

        session.commit()
        session.refresh(ejemplar)

        return ejemplar

    def eliminar(
        self,
        session: Session,
        id_ejemplar: uuid.UUID,
    ) -> bool:

        ejemplar = self.obtener_por_id(session, id_ejemplar)

        if ejemplar is None:
            return False

        session.delete(ejemplar)
        session.commit()

        return True