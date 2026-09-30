from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: str


class CategoriaUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None


class CategoriaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_categoria: UUID
    nombre: str
    descripcion: str


class CategoriaPost(BaseModel):
    data: CategoriaRead
    status: int
    message: str


class CategoriaList(BaseModel):
    data: list[CategoriaRead]
    status: int
    message: str


class CategoriaPut(BaseModel):
    data: CategoriaRead
    status: int
    message: str
