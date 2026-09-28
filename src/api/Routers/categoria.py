import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.categoria import CategoriaCrud
from src.database.connection import get_session
from src.schemas.categoria import (
    CategoriaCreate,
    CategoriaList,
    CategoriaPost,
    CategoriaPut,
    CategoriaUpdate,
)

router = APIRouter(prefix="/categorias", tags=["Categorías"])


def get_crud(session: Session = Depends(get_session)) -> CategoriaCrud:
    return CategoriaCrud(session)


@router.post("/", response_model=CategoriaPost, status_code=status.HTTP_201_CREATED)
def crear_categoria(payload: CategoriaCreate, crud: CategoriaCrud = Depends(get_crud)):
    categoria = crud.crear(
        nombre=payload.nombre,
        descripcion=payload.descripcion,
    )
    return {"data": categoria, "status": 201, "message": "Categoría creada correctamente"}


@router.get("/", response_model=CategoriaList)
def listar_categorias(crud: CategoriaCrud = Depends(get_crud)):
    categorias = crud.obtener_todos()
    return {
        "data": categorias,
        "status": 200,
        "message": "Categorías obtenidas correctamente",
    }


@router.get("/{id_categoria}", response_model=CategoriaPost)
def obtener_categoria(id_categoria: uuid.UUID, crud: CategoriaCrud = Depends(get_crud)):
    categoria = crud.obtener_por_id(id_categoria)

    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    return {"data": categoria, "status": 200, "message": "Categoría obtenida correctamente"}


@router.put("/{id_categoria}", response_model=CategoriaPut)
def actualizar_categoria(
    id_categoria: uuid.UUID,
    payload: CategoriaUpdate,
    crud: CategoriaCrud = Depends(get_crud),
):
    actual = crud.obtener_por_id(id_categoria)

    if actual is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # CategoriaUpdate es parcial, pero crud.actualizar exige todos los campos:
    # los que no vengan en el body se completan con el valor actual.
    cambios = payload.model_dump(exclude_none=True)

    categoria = crud.actualizar(
        id_categoria=id_categoria,
        nombre=cambios.get("nombre", actual.nombre),
        descripcion=cambios.get("descripcion", actual.descripcion),
    )

    return {
        "data": categoria,
        "status": 200,
        "message": "Categoría actualizada correctamente",
    }


@router.delete("/{id_categoria}")
def eliminar_categoria(id_categoria: uuid.UUID, crud: CategoriaCrud = Depends(get_crud)):
    try:
        eliminada = crud.eliminar(id_categoria)
    except IntegrityError:
        crud.session.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar la categoría porque tiene libros asociados",
        )

    if not eliminada:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    return {"status": 200, "message": "Categoría eliminada correctamente"}