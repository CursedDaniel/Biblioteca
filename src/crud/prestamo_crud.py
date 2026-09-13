import uuid
from datetime import date

from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.database import Base


class Prestamo(Base):
    __tablename__ = "prestamos"

    id_prestamo = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    id_usuario = Column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario"),
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
        default="activo",
    )

    usuario = relationship(
        "Usuario",
        back_populates="prestamos",
    )

    ejemplar = relationship(
        "Ejemplar",
        back_populates="prestamos",
    )

    multas = relationship(
        "Multa",
        back_populates="prestamo",
    )

    def __str__(self) -> str:
        return (
            f"ID: {self.id_prestamo}\n"
            f"ID Usuario: {self.id_usuario}\n"
            f"ID Ejemplar: {self.id_ejemplar}\n"
            f"Fecha de préstamo: {self.fecha_prestamo}\n"
            f"Fecha límite: {self.fecha_limite}\n"
            f"Fecha de devolución: {self.fecha_devolucion}\n"
            f"Estado: {self.estado}"
        )
        
