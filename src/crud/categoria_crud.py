import uuid

from sqlalchemy.orm import Session

from src.entities.categoria import Categoria


class CategoriaCrud:
    def __init__(self, session: Session):
        self.session = session

    def crear(
        self,
        nombre: str,
        descripcion: str,
    ) -> Categoria:
        categoria = Categoria(
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
        )

        self.session.add(categoria)
        self.session.commit()
        self.session.refresh(categoria)

        return categoria

    def obtener_por_id(
        self,
        id_categoria: uuid.UUID,
    ) -> Categoria | None:
        return self.session.get(Categoria, id_categoria)

    def obtener_por_nombre(
        self,
        nombre: str,
    ) -> Categoria | None:
        nombre_normalizado = nombre.strip().lower()

        categorias = self.session.query(Categoria).all()

        for categoria in categorias:
            if categoria.nombre.lower() == nombre_normalizado:
                return categoria

        return None

    def obtener_todos(self) -> list[Categoria]:
        return self.session.query(Categoria).all()

    def actualizar(
        self,
        id_categoria: uuid.UUID,
        nombre: str,
        descripcion: str,
    ) -> Categoria | None:
        categoria = self.obtener_por_id(id_categoria)

        if categoria is None:
            return None

        categoria.nombre = nombre.strip()
        categoria.descripcion = descripcion.strip()

        self.session.commit()
        self.session.refresh(categoria)

        return categoria

    def eliminar(self, id_categoria: uuid.UUID) -> bool:
        categoria = self.obtener_por_id(id_categoria)

        if categoria is None:
            return False

        self.session.delete(categoria)
        self.session.commit()

        return True
