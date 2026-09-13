import uuid
from datetime import date

from sqlalchemy.orm import Session

from src.entities.ejemplar import Ejemplar


class EjemplarCrud:
    def __init__(self, session: Session):
        self.session = session

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
            codigo_inventario=codigo_inventario.strip(),
            fecha_adquisicion=fecha_adquisicion,
            estado=estado.strip(),
            ubicacion=ubicacion.strip(),
        )

        self.session.add(ejemplar)
        self.session.commit()
        self.session.refresh(ejemplar)

        return ejemplar

    def obtener_por_id(self, id_ejemplar: uuid.UUID) -> Ejemplar | None:
        return self.session.get(Ejemplar, id_ejemplar)

    def obtener_por_codigo_inventario(self, codigo_inventario: str) -> Ejemplar | None:
        codigo_normalizado = codigo_inventario.strip()

        return (
            self.session.query(Ejemplar)
            .filter(Ejemplar.codigo_inventario.ilike(codigo_normalizado))
            .first()
        )

    def obtener_todos(self) -> list[Ejemplar]:
        return self.session.query(Ejemplar).all()

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

        self.session.commit()
        self.session.refresh(ejemplar)

        return ejemplar

    def eliminar(self, id_ejemplar: uuid.UUID) -> bool:
        ejemplar = self.obtener_por_id(id_ejemplar)

        if ejemplar is None:
            return False

        self.session.delete(ejemplar)
        self.session.commit()

        return True