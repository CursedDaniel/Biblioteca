import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.editorial_crud import EditorialCrud
from src.database.connection import get_session
from src.api.schemas.editorial import (
    EditorialCreate,
    EditorialList,
    EditorialPost,
    EditorialPut,
    EditorialUpdate,
)

router = APIRouter(prefix="/editoriales", tags=["Editoriales"])


def get_crud(session: Session = Depends(get_session)) -> EditorialCrud:
    return EditorialCrud(session)


@router.post("/", response_model=EditorialPost, status_code=status.HTTP_201_CREATED)
def crear_editorial(payload: EditorialCreate, crud: EditorialCrud = Depends(get_crud)):
    editorial = crud.crear(
        nombre=payload.nombre,
        pais=payload.pais,
        ciudad=payload.ciudad,
        telefono=payload.telefono,
        correo=payload.correo,
    )
    return {"data": editorial, "status": 201, "message": "Editorial creada correctamente"}


@router.get("/", response_model=EditorialList)
def listar_editoriales(crud: EditorialCrud = Depends(get_crud)):
    editoriales = crud.obtener_todos()
    return {
        "data": editoriales,
        "status": 200,
        "message": "Editoriales obtenidas correctamente",
    }


@router.get("/{id_editorial}", response_model=EditorialPost)
def obtener_editorial(id_editorial: uuid.UUID, crud: EditorialCrud = Depends(get_crud)):
    editorial = crud.obtener_por_id(id_editorial)

    if editorial is None:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")

    return {"data": editorial, "status": 200, "message": "Editorial obtenida correctamente"}


@router.put("/{id_editorial}", response_model=EditorialPut)
def actualizar_editorial(
    id_editorial: uuid.UUID,
    payload: EditorialUpdate,
    crud: EditorialCrud = Depends(get_crud),
):
    actual = crud.obtener_por_id(id_editorial)

    if actual is None:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")

    # EditorialUpdate es parcial, pero crud.actualizar exige todos los campos:
    # los que no vengan en el body se completan con el valor actual.
    cambios = payload.model_dump(exclude_none=True)

    editorial = crud.actualizar(
        id_editorial=id_editorial,
        nombre=cambios.get("nombre", actual.nombre),
        pais=cambios.get("pais", actual.pais),
        ciudad=cambios.get("ciudad", actual.ciudad),
        telefono=cambios.get("telefono", actual.telefono),
        correo=cambios.get("correo", actual.correo),
    )

    return {
        "data": editorial,
        "status": 200,
        "message": "Editorial actualizada correctamente",
    }


@router.delete("/{id_editorial}")
def eliminar_editorial(id_editorial: uuid.UUID, crud: EditorialCrud = Depends(get_crud)):
    try:
        eliminada = crud.eliminar(id_editorial)
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar la editorial porque tiene libros asociados",
        )

    if not eliminada:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")

    return {"status": 200, "message": "Editorial eliminada correctamente"}