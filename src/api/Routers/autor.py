import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.crud.autor import AutorCrud
from src.database.connection import get_session
from src.schemas.autor import (
    AutorCreate,
    AutorList,
    AutorPostResponse,
    AutorPutResponse,
    AutorUpdate,
)

router = APIRouter(prefix="/autores", tags=["Autores"])


def get_crud(session: Session = Depends(get_session)) -> AutorCrud:
    return AutorCrud(session)


@router.post("/", response_model=AutorPostResponse, status_code=status.HTTP_201_CREATED)
def crear_autor(payload: AutorCreate, crud: AutorCrud = Depends(get_crud)):
    autor = crud.crear(
        nombre=payload.nombre,
        apellido=payload.apellido,
        fecha_nacimiento=payload.fecha_nacimiento,
        nacionalidad=payload.nacionalidad,
        biografia=payload.biografia,
    )
    return {"data": autor, "status": 201, "message": "Autor creado correctamente"}


@router.get("/", response_model=AutorList)
def listar_autores(crud: AutorCrud = Depends(get_crud)):
    autores = crud.obtener_todos()
    return {
        "data": autores,
        "status": 200,
        "message": "Autores obtenidos correctamente",
    }


@router.get("/{id_autor}", response_model=AutorPostResponse)
def obtener_autor(id_autor: uuid.UUID, crud: AutorCrud = Depends(get_crud)):
    autor = crud.obtener_por_id(id_autor)

    if autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    return {"data": autor, "status": 200, "message": "Autor obtenido correctamente"}


@router.put("/{id_autor}", response_model=AutorPutResponse)
def actualizar_autor(
    id_autor: uuid.UUID,
    payload: AutorUpdate,
    crud: AutorCrud = Depends(get_crud),
):
    autor = crud.actualizar(
        id_autor=id_autor,
        nombre=payload.nombre,
        apellido=payload.apellido,
        fecha_nacimiento=payload.fecha_nacimiento,
        nacionalidad=payload.nacionalidad,
        biografia=payload.biografia,
    )

    if autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    return {"data": autor, "status": 200, "message": "Autor actualizado correctamente"}


@router.delete("/{id_autor}")
def eliminar_autor(id_autor: uuid.UUID, crud: AutorCrud = Depends(get_crud)):
    if not crud.eliminar(id_autor):
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    return {"status": 200, "message": "Autor eliminado correctamente"}
