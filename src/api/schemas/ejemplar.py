from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EjemplarCreate(BaseModel):
    id_libro: UUID
    codigo_inventario: str
    fecha_adquisicion: date | None = None
    estado: str
    ubicacion: str


class EjemplarUpdate(BaseModel):
    id_libro: UUID | None = None
    codigo_inventario: str | None = None
    fecha_adquisicion: date | None = None
    estado: str | None = None
    ubicacion: str | None = None


class EjemplarRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_ejemplar: UUID
    id_libro: UUID
    codigo_inventario: str
    fecha_adquisicion: date
    estado: str
    ubicacion: str


class EjemplarPost(BaseModel):
    data: EjemplarRead
    status: int
    message: str


class EjemplarList(BaseModel):
    data: list[EjemplarRead]
    status: int
    message: str


class EjemplarPut(BaseModel):
    data: EjemplarRead
    status: int
    message: str
