import uuid
from datetime import date

from sqlalchemy import Column, Date, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    nombre = Column(String(100), nullable=False)

    apellido = Column(String(100), nullable=False)

    documento = Column(String(30), nullable=False, unique=True)

    correo = Column(String(150), nullable=False, unique=True)

    telefono = Column(String(30), nullable=False)

    fecha_registro = Column(Date, nullable=False, default=date.today)

    estado = Column(String(20), nullable=False, default="activo")

    prestamos = relationship("Prestamo", back_populates="usuario")

    def __str__(self) -> str:
        return (
            f"ID: {self.id_usuario}\n"
            f"Nombre: {self.nombre}\n"
            f"Apellido: {self.apellido}\n"
            f"Documento: {self.documento}\n"
            f"Correo: {self.correo}\n"
            f"Teléfono: {self.telefono}\n"
            f"Fecha de registro: {self.fecha_registro}\n"
            f"Estado: {self.estado}"
        )
