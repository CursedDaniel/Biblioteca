from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AutorCreate(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: date
    nacionalidad: str
    biografia: str


class AutorUpdate(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: date
    nacionalidad: str
    biografia: str


class AutorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_autor: UUID
    nombre: str
    apellido: str
    fecha_nacimiento: date
    nacionalidad: str
    biografia: str


class AutorList(BaseModel):
    data: list[AutorRead]
    status: int
    message: str


class AutorPost(BaseModel):
    data: AutorRead
    status: int
    message: str


class AutorPut(BaseModel):
    data: AutorRead
    status: int
    message: str
