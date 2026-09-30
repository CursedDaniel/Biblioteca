import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.ejemplar_crud import EjemplarCrud
from src.database.connection import get_session
from src.api.schemas.ejemplar import (
    EjemplarCreate,
    EjemplarList,
    EjemplarPost,
    EjemplarPut,
    EjemplarUpdate,
)

router = APIRouter(prefix="/ejemplares", tags=["Ejemplares"])


def get_crud(session: Session = Depends(get_session)) -> EjemplarCrud:
    return EjemplarCrud(session)


@router.post("/", response_model=EjemplarPost, status_code=status.HTTP_201_CREATED)
def crear_ejemplar(payload: EjemplarCreate, crud: EjemplarCrud = Depends(get_crud)):
    try:
        ejemplar = crud.crear(
            id_libro=payload.id_libro,
            codigo_inventario=payload.codigo_inventario,
            # En el schema es opcional, pero crud.crear espera un date
            fecha_adquisicion=payload.fecha_adquisicion or date.today(),
            estado=payload.estado,
            ubicacion=payload.ubicacion,
        )
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="El código de inventario ya existe o el libro indicado no existe",
        )

    return {"data": ejemplar, "status": 201, "message": "Ejemplar creado correctamente"}


@router.get("/", response_model=EjemplarList)
def listar_ejemplares(crud: EjemplarCrud = Depends(get_crud)):
    ejemplares = crud.obtener_todos()
    return {
        "data": ejemplares,
        "status": 200,
        "message": "Ejemplares obtenidos correctamente",
    }


@router.get("/{id_ejemplar}", response_model=EjemplarPost)
def obtener_ejemplar(id_ejemplar: uuid.UUID, crud: EjemplarCrud = Depends(get_crud)):
    ejemplar = crud.obtener_por_id(id_ejemplar)

    if ejemplar is None:
        raise HTTPException(status_code=404, detail="Ejemplar no encontrado")

    return {"data": ejemplar, "status": 200, "message": "Ejemplar obtenido correctamente"}


@router.put("/{id_ejemplar}", response_model=EjemplarPut)
def actualizar_ejemplar(
    id_ejemplar: uuid.UUID,
    payload: EjemplarUpdate,
    crud: EjemplarCrud = Depends(get_crud),
):
    actual = crud.obtener_por_id(id_ejemplar)

    if actual is None:
        raise HTTPException(status_code=404, detail="Ejemplar no encontrado")

    # EjemplarUpdate es parcial, pero crud.actualizar exige todos los campos:
    # los que no vengan en el body se completan con el valor actual.
    cambios = payload.model_dump(exclude_none=True)

    try:
        ejemplar = crud.actualizar(
            id_ejemplar=id_ejemplar,
            id_libro=cambios.get("id_libro", actual.id_libro),
            codigo_inventario=cambios.get("codigo_inventario", actual.codigo_inventario),
            fecha_adquisicion=cambios.get("fecha_adquisicion", actual.fecha_adquisicion),
            estado=cambios.get("estado", actual.estado),
            ubicacion=cambios.get("ubicacion", actual.ubicacion),
        )
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="El código de inventario ya existe o el libro indicado no existe",
        )

    return {
        "data": ejemplar,
        "status": 200,
        "message": "Ejemplar actualizado correctamente",
    }


@router.delete("/{id_ejemplar}")
def eliminar_ejemplar(id_ejemplar: uuid.UUID, crud: EjemplarCrud = Depends(get_crud)):
    try:
        eliminado = crud.eliminar(id_ejemplar)
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el ejemplar porque tiene préstamos o multas asociados",
        )

    if not eliminado:
        raise HTTPException(status_code=404, detail="Ejemplar no encontrado")

    return {"status": 200, "message": "Ejemplar eliminado correctamente"}