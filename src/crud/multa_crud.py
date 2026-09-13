import uuid
from datetime import date

from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.database import Base


class Multa(Base):
    __tablename__ = "multas"

    id_multa = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    id_prestamo = Column(
        UUID(as_uuid=True),
        ForeignKey("prestamos.id_prestamo"),
        nullable=False,
    )

    id_ejemplar = Column(
        UUID(as_uuid=True),
        ForeignKey("ejemplares.id_ejemplar"),
        nullable=False,
    )

    fecha_prestamo = Column(Date, nullable=False)
    fecha_limite = Column(Date, nullable=False)
    fecha_devolucion = Column(Date, nullable=True)
    estado = Column(
        String(20),
        nullable=False,
        default="pendiente",
    )

    prestamo = relationship(
        "Prestamo",
        back_populates="multas",
    )

    ejemplar = relationship(
        "Ejemplar",
        back_populates="multas",
    )

    def __str__(self) -> str:
        return (
            f"ID: {self.id_multa}\n"
            f"ID Préstamo: {self.id_prestamo}\n"
            f"ID Ejemplar: {self.id_ejemplar}\n"
            f"Fecha de préstamo: {self.fecha_prestamo}\n"
            f"Fecha límite: {self.fecha_limite}\n"
            f"Fecha de devolución: {self.fecha_devolucion}\n"
            f"Estado: {self.estado}"
        )
