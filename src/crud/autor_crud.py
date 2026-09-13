import uuid

from datetime import date

from sqlalchemy.orm import Session

from src.entities.autor import Autor


class AutorCrud:
    def __init__(self, session: Session):
        self.session = session

    def crear(
        self,
        nombre: str,
        apellido: str,
        fecha_nacimiento: date,
        nacionalidad: str,
        biografia: str,
    ) -> Autor:
        autor = Autor(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            fecha_nacimiento=fecha_nacimiento,
            nacionalidad=nacionalidad.strip(),
            biografia=biografia.strip(),
        )

        self.session.add(autor)
        self.session.commit()
        self.session.refresh(autor)

        return autor

    def obtener_por_id(
        self,
        id_autor: uuid.UUID,
    ) -> Autor | None:
        return self.session.get(Autor, id_autor)

    def obtener_todos(self) -> list[Autor]:
        return self.session.query(Autor).all()

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

        self.session.commit()
        self.session.refresh(autor)

        return autor

    def eliminar(self, id_autor: uuid.UUID) -> bool:
        autor = self.obtener_por_id(id_autor)

        if autor is None:
            return False

        self.session.delete(autor)
        self.session.commit()

        return True
