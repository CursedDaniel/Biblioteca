from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PrestamoCreate(BaseModel):
    id_usuario: UUID
    id_ejemplar: UUID
    fecha_prestamo: date
    fecha_limite: date
    fecha_devolucion: date | None = None
    estado: str = "activo"


class PrestamoUpdate(BaseModel):
    id_usuario: UUID | None = None
    id_ejemplar: UUID | None = None
    fecha_prestamo: date | None = None
    fecha_limite: date | None = None
    fecha_devolucion: date | None = None
    estado: str | None = None


class PrestamoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_prestamo: UUID
    id_usuario: UUID
    id_ejemplar: UUID
    fecha_prestamo: date
    fecha_limite: date
    fecha_devolucion: date | None
    estado: str


class PrestamoPost(BaseModel):
    data: PrestamoRead
    status: int
    message: str


class PrestamoList(BaseModel):
    data: list[PrestamoRead]
    status: int
    message: str


class PrestamoPut(BaseModel):
    data: PrestamoRead
    status: int
    message: str
