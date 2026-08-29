import uuid

from src.entities.categoria import Categoria


class CategoriaCrud:
    def __init__(self):
        self.categorias: list[Categoria] = []

    def crear(
        self,
        nombre: str,
        descripcion: str,
    ) -> Categoria:
        categoria = Categoria(
            nombre=nombre,
            descripcion=descripcion,
        )

        self.categorias.append(categoria)
        return categoria

    def obtener_por_id(
        self,
        id_categoria: uuid.UUID,
    ) -> Categoria | None:
        for categoria in self.categorias:
            if categoria.id_categoria == id_categoria:
                return categoria

        return None

    def obtener_por_nombre(self, nombre: str) -> Categoria | None:
        nombre_normalizado = nombre.strip().lower()

        for categoria in self.categorias:
            if categoria.nombre.lower() == nombre_normalizado:
                return categoria

        return None

    def obtener_todos(self) -> list[Categoria]:
        return self.categorias

    def obtener_por_nombre(self, nombre: str) -> Categoria | None:
        nombre_normalizado = nombre.strip().lower()

        for categoria in self.categorias:
            if categoria.nombre.lower() == nombre_normalizado:
                return categoria

        return None

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

        return categoria

    def eliminar(self, id_categoria: uuid.UUID) -> bool:
        categoria = self.obtener_por_id(id_categoria)

        if categoria is None:
            return False

        self.categorias.remove(categoria)
        return True
