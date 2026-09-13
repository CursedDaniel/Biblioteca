import uuid
from datetime import date

from sqlalchemy import Column, Date, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.database import Base
from src.database.libro_autor import libro_autor


import uuid
from datetime import date

from sqlalchemy import Column, Date, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.database import Base
from src.database.libro_autor import libro_autor


class Autor(Base):
    __tablename__ = "autores"

    id_autor = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    nacionalidad = Column(String(100), nullable=False)
    biografia = Column(Text, nullable=False)

    libros = relationship("Libro", secondary=libro_autor, back_populates="autores")

    def __str__(self) -> str:
        return (
            f"ID: {self.id_autor}\n"
            f"Nombre: {self.nombre}\n"
            f"Apellido: {self.apellido}\n"
            f"Fecha de Nacimiento: {self.fecha_nacimiento}\n"
            f"Nacionalidad: {self.nacionalidad}\n"
            f"Biografía: {self.biografia}"
        )
