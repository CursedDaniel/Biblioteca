import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.multa import MultaCrud
from src.database.connection import get_session
from src.schemas.multa import (
    MultaCreate,
    MultaList,
    MultaPost,
    MultaPut,
    MultaUpdate,
)

router = APIRouter(prefix="/multas", tags=["Multas"])


def get_crud(session: Session = Depends(get_session)) -> MultaCrud:
    return MultaCrud(session)


@router.post("/", response_model=MultaPost, status_code=status.HTTP_201_CREATED)
def crear_multa(payload: MultaCreate, crud: MultaCrud = Depends(get_crud)):
    try:
        multa = crud.crear(
            id_prestamo=payload.id_prestamo,
            id_ejemplar=payload.id_ejemplar,
            fecha_prestamo=payload.fecha_prestamo,
            fecha_limite=payload.fecha_limite,
            fecha_devolucion=payload.fecha_devolucion,
            estado=payload.estado,
        )
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="El préstamo o el ejemplar indicado no existe",
        )

    return {"data": multa, "status": 201, "message": "Multa creada correctamente"}


@router.get("/", response_model=MultaList)
def listar_multas(crud: MultaCrud = Depends(get_crud)):
    multas = crud.obtener_todos()
    return {"data": multas, "status": 200, "message": "Multas obtenidas correctamente"}


@router.get("/{id_multa}", response_model=MultaPost)
def obtener_multa(id_multa: uuid.UUID, crud: MultaCrud = Depends(get_crud)):
    multa = crud.obtener_por_id(id_multa)

    if multa is None:
        raise HTTPException(status_code=404, detail="Multa no encontrada")

    return {"data": multa, "status": 200, "message": "Multa obtenida correctamente"}


@router.put("/{id_multa}", response_model=MultaPut)
def actualizar_multa(
    id_multa: uuid.UUID,
    payload: MultaUpdate,
    crud: MultaCrud = Depends(get_crud),
):
    actual = crud.obtener_por_id(id_multa)

    if actual is None:
        raise HTTPException(status_code=404, detail="Multa no encontrada")

    # MultaUpdate es parcial, pero crud.actualizar exige todos los campos:
    # los que no vengan en el body se completan con el valor actual.
    cambios = payload.model_dump(exclude_none=True)

    # fecha_devolucion es nullable: si el cliente la envía explícitamente
    # como null, se respeta (permite "des-devolver"); si no la envía, se conserva.
    if "fecha_devolucion" in payload.model_fields_set:
        fecha_devolucion = payload.fecha_devolucion
    else:
        fecha_devolucion = actual.fecha_devolucion

    try:
        multa = crud.actualizar(
            id_multa=id_multa,
            id_prestamo=cambios.get("id_prestamo", actual.id_prestamo),
            id_ejemplar=cambios.get("id_ejemplar", actual.id_ejemplar),
            fecha_prestamo=cambios.get("fecha_prestamo", actual.fecha_prestamo),
            fecha_limite=cambios.get("fecha_limite", actual.fecha_limite),
            fecha_devolucion=fecha_devolucion,
            estado=cambios.get("estado", actual.estado),
        )
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="El préstamo o el ejemplar indicado no existe",
        )

    return {"data": multa, "status": 200, "message": "Multa actualizada correctamente"}


@router.delete("/{id_multa}")
def eliminar_multa(id_multa: uuid.UUID, crud: MultaCrud = Depends(get_crud)):
    if not crud.eliminar(id_multa):
        raise HTTPException(status_code=404, detail="Multa no encontrada")

    return {"status": 200, "message": "Multa eliminada correctamente"}