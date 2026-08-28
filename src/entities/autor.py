# comienzo entidad autor

import uuid
from datetime import date

class autor:
    def __init__(
        self,
        nombre: str,
        apellido: str,
        fecha_nacimiento: date,
        nacionalidad: str,
        biografia: str,
        id_autor: uuid.UUID | None = None,
    ):
        
        self.id_autor = id_autor if id_autor is not None else uuid.uuid4()
        self.nombre = nombre.strip()
        self.apellido = apellido.strip()
        self.fecha_nacimiento = fecha_nacimiento
        self.nacionalidad = nacionalidad.strip()
        self.biografia = biografia.strip()
        
    def __str__(self) -> str:
        return (
            f"ID: {self.id_autor}\n"
            f"Nombre: {self.nombre}\n"
            f"Apellido: {self.apellido}\n"
            f"Fecha de Nacimiento: {self.fecha_nacimiento}\n"
            f"Nacionalidad: {self.nacionalidad}\n"
            f"Biografía: {self.biografia}"
        )