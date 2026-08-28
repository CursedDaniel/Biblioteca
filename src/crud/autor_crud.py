import uuid
from datetime import date

from src.entities.autor import Autor


class AutorCrud:
    def __init__(self):
        self.autores: list[Autor] = []

    def crear(
        self,
        nombre: str,
        apellido: str,
        fecha_nacimiento: date,
        nacionalidad: str,
        biografia: str,
    ) -> Autor:
        autor = Autor(
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            nacionalidad=nacionalidad,
            biografia=biografia,
        )

        self.autores.append(autor)
        return autor

    def obtener_por_id(
        self,
        id_autor: uuid.UUID,
    ) -> Autor | None:
        for autor in self.autores:
            if autor.id_autor == id_autor:
                return autor

        return None

    def obtener_todos(self) -> list[Autor]:
        return self.autores

    def actualizar(
        self,
        id_autor: uuid.UUID,
        nombre: str,
        apellido: str,
        fecha_nacimiento: date,
        nacionalidad: str,
        biografia: str,
    ) -> Autor | None:
        autor = self.obtener_por_id(id_autor)

        if autor is None:
            return None

        autor.nombre = nombre.strip()
        autor.apellido = apellido.strip()
        autor.fecha_nacimiento = fecha_nacimiento
        autor.nacionalidad = nacionalidad.strip()
        autor.biografia = biografia.strip()

        return autor

    def eliminar(self, id_autor: uuid.UUID) -> bool:
        autor = self.obtener_por_id(id_autor)

        if autor is None:
            return False

        self.autores.remove(autor)
        return True
