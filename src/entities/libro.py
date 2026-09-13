import uuid

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.database import Base
from src.database.libro_autor import libro_autor


class Libro(Base):
    __tablename__ = "libros"

    id_libro = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    titulo = Column(String(200), nullable=False)

    fecha_publicacion = Column(Date, nullable=False)

    numero_paginas = Column(Integer, nullable=False)

    idiomas = Column(String(100), nullable=False)

    descripcion = Column(Text, nullable=False)

    id_categoria = Column(
        UUID(as_uuid=True), ForeignKey("categorias.id_categoria"), nullable=False
    )

    id_editorial = Column(
        UUID(as_uuid=True), ForeignKey("editoriales.id_editorial"), nullable=False
    )

    categoria = relationship("Categoria", back_populates="libros")

    editorial = relationship("Editorial", back_populates="libros")

    autores = relationship("Autor", secondary=libro_autor, back_populates="libros")

    ejemplares = relationship("Ejemplar", back_populates="libro")

    def __str__(self) -> str:
        return (
            f"ID: {self.id_libro}\n"
            f"Título: {self.titulo}\n"
            f"Fecha de Publicación: {self.fecha_publicacion}\n"
            f"Número de Páginas: {self.numero_paginas}\n"
            f"Idiomas: {self.idiomas}\n"
            f"Descripción: {self.descripcion}\n"
            f"ID Categoría: {self.id_categoria}\n"
            f"ID Editorial: {self.id_editorial}"
        )
