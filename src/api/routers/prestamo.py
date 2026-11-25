import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.prestamo_crud import PrestamoCrud
from src.database.connection import get_session
from src.api.schemas.prestamo import (
    PrestamoCreate,
    PrestamoList,
    PrestamoPost,
    PrestamoPut,
    PrestamoUpdate,
)

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])


def get_crud(session: Session = Depends(get_session)) -> PrestamoCrud:
    return PrestamoCrud(session)


@router.post("/", response_model=PrestamoPost, status_code=status.HTTP_201_CREATED)
def crear_prestamo(payload: PrestamoCreate, crud: PrestamoCrud = Depends(get_crud)):
    try:
        prestamo = crud.crear(
            id_usuario=payload.id_usuario,
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
            detail="El usuario o el ejemplar indicado no existe",
        )

    return {"data": prestamo, "status": 201, "message": "Préstamo creado correctamente"}


@router.get("/", response_model=PrestamoList)
def listar_prestamos(crud: PrestamoCrud = Depends(get_crud)):
    prestamos = crud.obtener_todos()
    return {
        "data": prestamos,
        "status": 200,
        "message": "Préstamos obtenidos correctamente",
    }


@router.get("/{id_prestamo}", response_model=PrestamoPost)
def obtener_prestamo(id_prestamo: uuid.UUID, crud: PrestamoCrud = Depends(get_crud)):
    prestamo = crud.obtener_por_id(id_prestamo)

    if prestamo is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    return {"data": prestamo, "status": 200, "message": "Préstamo obtenido correctamente"}


@router.put("/{id_prestamo}", response_model=PrestamoPut)
def actualizar_prestamo(
    id_prestamo: uuid.UUID,
    payload: PrestamoUpdate,
    crud: PrestamoCrud = Depends(get_crud),
):
    actual = crud.obtener_por_id(id_prestamo)

    if actual is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    # PrestamoUpdate es parcial, pero crud.actualizar exige todos los campos:
    # los que no vengan en el body se completan con el valor actual.
    cambios = payload.model_dump(exclude_none=True)

    # fecha_devolucion es nullable: si el cliente la envía explícitamente
    # como null, se respeta; si no la envía, se conserva la actual.
    if "fecha_devolucion" in payload.model_fields_set:
        fecha_devolucion = payload.fecha_devolucion
    else:
        fecha_devolucion = actual.fecha_devolucion

    try:
        prestamo = crud.actualizar(
            id_prestamo=id_prestamo,
            id_usuario=cambios.get("id_usuario", actual.id_usuario),
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
            detail="El usuario o el ejemplar indicado no existe",
        )

    return {
        "data": prestamo,
        "status": 200,
        "message": "Préstamo actualizado correctamente",
    }


@router.delete("/{id_prestamo}")
def eliminar_prestamo(id_prestamo: uuid.UUID, crud: PrestamoCrud = Depends(get_crud)):
    try:
        eliminado = crud.eliminar(id_prestamo)
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el préstamo porque tiene multas asociadas",
        )

    if not eliminado:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    return {"status": 200, "message": "Préstamo eliminado correctamente"}