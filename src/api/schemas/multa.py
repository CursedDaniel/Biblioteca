from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MultaCreate(BaseModel):
    fecha_prestamo: date
    fecha_limite: date
    fecha_devolucion: date | None = None
    estado: str
    id_prestamo: UUID
    id_ejemplar: UUID


class MultaUpdate(BaseModel):
    fecha_prestamo: date | None = None
    fecha_limite: date | None = None
    fecha_devolucion: date | None = None
    estado: str | None = None
    id_prestamo: UUID | None = None
    id_ejemplar: UUID | None = None


class MultaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_multa: UUID
    fecha_prestamo: date
    fecha_limite: date
    fecha_devolucion: date | None
    estado: str
    id_prestamo: UUID
    id_ejemplar: UUID


class MultaPost(BaseModel):
    data: MultaRead
    status: int
    message: str


class MultaList(BaseModel):
    data: list[MultaRead]
    status: int
    message: str


class MultaPut(BaseModel):
    data: MultaRead
    status: int
    message: str
