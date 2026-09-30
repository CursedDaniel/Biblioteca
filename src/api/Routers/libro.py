import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.libro_crud import LibroCrud
from src.database.connection import get_session
from src.api.schemas.libro import (
    LibroCreate,
    LibroList,
    LibroPost,
    LibroPut,
    LibroUpdate,
)

router = APIRouter(prefix="/libros", tags=["Libros"])


def get_crud(session: Session = Depends(get_session)) -> LibroCrud:
    return LibroCrud(session)


@router.post("/", response_model=LibroPost, status_code=status.HTTP_201_CREATED)
def crear_libro(payload: LibroCreate, crud: LibroCrud = Depends(get_crud)):
    try:
        libro = crud.crear(
            titulo=payload.titulo,
            fecha_publicacion=payload.fecha_publicacion,
            numero_paginas=payload.numero_paginas,
            idiomas=payload.idiomas,
            descripcion=payload.descripcion,
            id_categoria=payload.id_categoria,
            id_editorial=payload.id_editorial,
        )
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="La categoría o la editorial indicada no existe",
        )

    return {"data": libro, "status": 201, "message": "Libro creado correctamente"}


@router.get("/", response_model=LibroList)
def listar_libros(crud: LibroCrud = Depends(get_crud)):
    libros = crud.obtener_todos()
    return {"data": libros, "status": 200, "message": "Libros obtenidos correctamente"}


@router.get("/{id_libro}", response_model=LibroPost)
def obtener_libro(id_libro: uuid.UUID, crud: LibroCrud = Depends(get_crud)):
    libro = crud.obtener_por_id(id_libro)

    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return {"data": libro, "status": 200, "message": "Libro obtenido correctamente"}


@router.put("/{id_libro}", response_model=LibroPut)
def actualizar_libro(
    id_libro: uuid.UUID,
    payload: LibroUpdate,
    crud: LibroCrud = Depends(get_crud),
):
    actual = crud.obtener_por_id(id_libro)

    if actual is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    # LibroUpdate es parcial, pero crud.actualizar exige todos los campos:
    # los que no vengan en el body se completan con el valor actual.
    cambios = payload.model_dump(exclude_none=True)

    try:
        libro = crud.actualizar(
            id_libro=id_libro,
            titulo=cambios.get("titulo", actual.titulo),
            fecha_publicacion=cambios.get("fecha_publicacion", actual.fecha_publicacion),
            numero_paginas=cambios.get("numero_paginas", actual.numero_paginas),
            idiomas=cambios.get("idiomas", actual.idiomas),
            descripcion=cambios.get("descripcion", actual.descripcion),
            id_categoria=cambios.get("id_categoria", actual.id_categoria),
            id_editorial=cambios.get("id_editorial", actual.id_editorial),
        )
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="La categoría o la editorial indicada no existe",
        )

    return {"data": libro, "status": 200, "message": "Libro actualizado correctamente"}


@router.delete("/{id_libro}")
def eliminar_libro(id_libro: uuid.UUID, crud: LibroCrud = Depends(get_crud)):
    try:
        eliminado = crud.eliminar(id_libro)
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el libro porque tiene ejemplares asociados",
        )

    if not eliminado:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return {"status": 200, "message": "Libro eliminado correctamente"}