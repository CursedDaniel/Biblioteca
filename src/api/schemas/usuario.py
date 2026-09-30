from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict  # pyright: ignore[reportMissingImports]


class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    documento: str
    correo: str
    telefono: str
    fecha_registro: date
    estado: str


class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    documento: str | None = None
    correo: str | None = None
    telefono: str | None = None
    fecha_registro: date | None = None
    estado: str | None = None


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: UUID
    nombre: str
    apellido: str
    documento: str
    correo: str
    telefono: str
    fecha_registro: date
    estado: str


class UsuarioPost(BaseModel):

    data: UsuarioRead
    status: int
    message: str


class UsuarioList(BaseModel):
    data: list[UsuarioRead]
    status: int
    message: str


class UsuarioPut(BaseModel):
    data: UsuarioRead
    status: int
    message: str
