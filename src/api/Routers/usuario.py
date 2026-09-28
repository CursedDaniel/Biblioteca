import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.usuario import UsuarioCrud
from src.database.connection import get_session
from src.schemas.usuario import (
    UsuarioCreate,
    UsuarioList,
    UsuarioPost,
    UsuarioPut,
    UsuarioUpdate,
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def get_crud(session: Session = Depends(get_session)) -> UsuarioCrud:
    return UsuarioCrud(session)


@router.post("/", response_model=UsuarioPost, status_code=status.HTTP_201_CREATED)
def crear_usuario(payload: UsuarioCreate, crud: UsuarioCrud = Depends(get_crud)):
    try:
        usuario = crud.crear(
            nombre=payload.nombre,
            apellido=payload.apellido,
            documento=payload.documento,
            correo=payload.correo,
            telefono=payload.telefono,
            fecha_registro=payload.fecha_registro,
            estado=payload.estado,
        )
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ya existe un usuario con ese documento o correo",
        )

    return {"data": usuario, "status": 201, "message": "Usuario creado correctamente"}


@router.get("/", response_model=UsuarioList)
def listar_usuarios(crud: UsuarioCrud = Depends(get_crud)):
    usuarios = crud.obtener_todos()
    return {
        "data": usuarios,
        "status": 200,
        "message": "Usuarios obtenidos correctamente",
    }


@router.get("/{id_usuario}", response_model=UsuarioPost)
def obtener_usuario(id_usuario: uuid.UUID, crud: UsuarioCrud = Depends(get_crud)):
    usuario = crud.obtener_por_id(id_usuario)

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"data": usuario, "status": 200, "message": "Usuario obtenido correctamente"}


@router.put("/{id_usuario}", response_model=UsuarioPut)
def actualizar_usuario(
    id_usuario: uuid.UUID,
    payload: UsuarioUpdate,
    crud: UsuarioCrud = Depends(get_crud),
):
    actual = crud.obtener_por_id(id_usuario)

    if actual is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # UsuarioUpdate es parcial, pero crud.actualizar exige todos los campos:
    # los que no vengan en el body se completan con el valor actual.
    cambios = payload.model_dump(exclude_none=True)

    try:
        usuario = crud.actualizar(
            id_usuario=id_usuario,
            nombre=cambios.get("nombre", actual.nombre),
            apellido=cambios.get("apellido", actual.apellido),
            documento=cambios.get("documento", actual.documento),
            correo=cambios.get("correo", actual.correo),
            telefono=cambios.get("telefono", actual.telefono),
            fecha_registro=cambios.get("fecha_registro", actual.fecha_registro),
            estado=cambios.get("estado", actual.estado),
        )
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ya existe un usuario con ese documento o correo",
        )

    return {
        "data": usuario,
        "status": 200,
        "message": "Usuario actualizado correctamente",
    }


@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: uuid.UUID, crud: UsuarioCrud = Depends(get_crud)):
    try:
        eliminado = crud.eliminar(id_usuario)
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el usuario porque tiene préstamos asociados",
        )

    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"status": 200, "message": "Usuario eliminado correctamente"}