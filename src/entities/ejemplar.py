import uuid
from datetime import date

from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.database import Base


class Ejemplar(Base):
    __tablename__ = "ejemplares"

    id_ejemplar = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    id_libro = Column(UUID(as_uuid=True), ForeignKey("libros.id_libro"), nullable=False)

    codigo_inventario = Column(String(50), nullable=False, unique=True)

    fecha_adquisicion = Column(Date, nullable=False, default=date.today)

    estado = Column(String(30), nullable=False)

    ubicacion = Column(String(100), nullable=False)

    libro = relationship("Libro", back_populates="ejemplares")

    def __str__(self) -> str:
        return (
            f"ID: {self.id_ejemplar}\n"
            f"ID Libro: {self.id_libro}\n"
            f"Código de Inventario: {self.codigo_inventario}\n"
            f"Fecha de Adquisición: {self.fecha_adquisicion}\n"
            f"Estado: {self.estado}\n"
            f"Ubicación: {self.ubicacion}"
        )
