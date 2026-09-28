from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LibroCreate(BaseModel):
    titulo: str
    fecha_publicacion: date
    numero_paginas: int
    idiomas: str
    descripcion: str
    id_categoria: UUID
    id_editorial: UUID


class LibroUpdate(BaseModel):
    titulo: str | None = None
    fecha_publicacion: date | None = None
    numero_paginas: int | None = None
    idiomas: str | None = None
    descripcion: str | None = None
    id_categoria: UUID | None = None
    id_editorial: UUID | None = None


class LibroRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_libro: UUID
    titulo: str
    fecha_publicacion: date
    numero_paginas: int
    idiomas: str
    descripcion: str
    id_categoria: UUID
    id_editorial: UUID


class LibroPost(BaseModel):
    data: LibroRead
    status: int
    message: str


class LibroList(BaseModel):
    data: list[LibroRead]
    status: int
    message: str


class LibroPut(BaseModel):
    data: LibroRead
    status: int
    message: str
