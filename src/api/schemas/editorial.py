from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EditorialCreate(BaseModel):
    nombre: str
    pais: str
    ciudad: str
    correo: str
    telefono: str


class EditorialUpdate(BaseModel):
    nombre: str | None = None
    pais: str | None = None
    ciudad: str | None = None
    correo: str | None = None
    telefono: str | None = None


class EditorialRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_editorial: UUID
    nombre: str
    pais: str
    ciudad: str
    correo: str
    telefono: str


class EditorialPost(BaseModel):
    data: EditorialRead
    status: int
    message: str


class EditorialList(BaseModel):
    data: list[EditorialRead]
    status: int
    message: str


class EditorialPut(BaseModel):
    data: EditorialRead
    status: int
    message: str
