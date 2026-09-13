import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)

    libros = relationship("Libro", back_populates="categoria")

    def __str__(self) -> str:
        return (
            f"ID: {self.id_categoria}\n"
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}"
        )