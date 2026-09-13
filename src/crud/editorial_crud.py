import uuid
from sqlalchemy.orm import Session
from src.entities.editorial import Editorial


class EditorialCrud:

    def __init__(self, session: Session):
        self.session = session

    def crear(
        self,
        nombre: str,
        pais: str,
        ciudad: str,
        telefono: str,
        correo: str,
    ) -> Editorial:
        editorial = Editorial(
            nombre=nombre.strip(),
            pais=pais.strip(),
            ciudad=ciudad.strip(),
            telefono=telefono.strip(),
            correo=correo.strip(),
        )

        self.session.add(editorial)
        self.session.commit()
        self.session.refresh(editorial)

        return editorial

    def obtener_por_id(self, id_editorial: uuid.UUID) -> Editorial | None:
        return self.session.get(Editorial, id_editorial)

    def obtener_por_nombre(self, nombre: str) -> Editorial | None:
        nombre_normalizado = nombre.strip()

        return (
            self.session.query(Editorial)
            .filter(Editorial.nombre.ilike(nombre_normalizado))
            .first()
        )

    def obtener_todos(self) -> list[Editorial]:
        return self.session.query(Editorial).all()

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

        self.session.commit()
        self.session.refresh(editorial)

        return editorial

    def eliminar(self, id_editorial: uuid.UUID) -> bool:
        editorial = self.obtener_por_id(id_editorial)

        if editorial is None:
            return False

        self.session.delete(editorial)
        self.session.commit()

        return True
