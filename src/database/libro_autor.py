from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from src.database.database import Base

libro_autor = Table(
    "libro_autor",
    Base.metadata,
    Column(
        "id_libro",
        UUID(as_uuid=True),
        ForeignKey("libros.id_libro"),
        primary_key=True,
    ),
    Column(
        "id_autor",
        UUID(as_uuid=True),
        ForeignKey("autores.id_autor"),
        primary_key=True,
    ),
)