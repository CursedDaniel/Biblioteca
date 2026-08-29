import uuid

from src.entities.editorial import Editorial


class EditorialCrud:
    def __init__(self):
        self.editoriales: list[Editorial] = []

    def crear(
        self,
        nombre: str,
        pais: str,
        ciudad: str,
        telefono: str,
        correo: str,
    ) -> Editorial:
        editorial = Editorial(
            nombre=nombre,
            pais=pais,
            ciudad=ciudad,
            telefono=telefono,
            correo=correo,
        )

        self.editoriales.append(editorial)
        return editorial

    def obtener_por_id(
        self,
        id_editorial: uuid.UUID,
    ) -> Editorial | None:
        for editorial in self.editoriales:
            if editorial.id_editorial == id_editorial:
                return editorial

        return None

    def obtener_por_nombre(self, nombre: str) -> Editorial | None:
        nombre_normalizado = nombre.strip().lower()

        for editorial in self.editoriales:
            if editorial.nombre.lower() == nombre_normalizado:
                return editorial

        return None

    def obtener_todos(self) -> list[Editorial]:
        return self.editoriales

    def actualizar(
        self,
        id_editorial: uuid.UUID,
        nombre: str,
        pais: str,
        ciudad: str,
        telefono: str,
        correo: str,
    ) -> Editorial | None:
        editorial = self.obtener_por_id(id_editorial)

        if editorial is None:
            return None

        editorial.nombre = nombre.strip()
        editorial.pais = pais.strip()
        editorial.ciudad = ciudad.strip()
        editorial.telefono = telefono.strip()
        editorial.correo = correo.strip()

        return editorial

    def eliminar(self, id_editorial: uuid.UUID) -> bool:
        editorial = self.obtener_por_id(id_editorial)

        if editorial is None:
            return False

        self.editoriales.remove(editorial)
        return True
