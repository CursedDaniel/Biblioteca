import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.database import Base


class Editorial(Base):
    __tablename__ = "editoriales"

    id_editorial = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    nombre = Column(String(150), nullable=False)
    pais = Column(String(80), nullable=False)
    ciudad = Column(String(80), nullable=False)
    correo = Column(String(150), nullable=False)
    telefono = Column(String(30), nullable=False)

    libros = relationship("Libro", back_populates="editorial")

    def __str__(self) -> str:
        return (
            f"ID: {self.id_editorial}\n"
            f"Nombre: {self.nombre}\n"
            f"País: {self.pais}\n"
            f"Ciudad: {self.ciudad}\n"
            f"Correo: {self.correo}\n"
            f"Teléfono: {self.telefono}"
        )