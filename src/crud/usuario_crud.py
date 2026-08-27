import uuid
from datetime import date

from src.entities.usuario import Usuario


class UsuarioCrud:
    def __init__(self):
        self.usuarios: list[Usuario] = []

    def crear(
        self,
        nombre: str,
        apellido: str,
        documento: str,
        correo: str,
        telefono: str,
        fecha_registro: date,
        estado: str,
    ) -> Usuario:
        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            documento=documento,
            correo=correo,
            telefono=telefono,
            fecha_registro=fecha_registro,
            estado=estado,
        )

        self.usuarios.append(usuario)
        return usuario

    def obtener_por_id(
        self,
        id_usuario: uuid.UUID,
    ) -> Usuario | None:
        for usuario in self.usuarios:
            if usuario.id_usuario == id_usuario:
                return usuario

        return None

    def obtener_todos(self) -> list[Usuario]:
        return self.usuarios

    def actualizar(
        self,
        id_usuario: uuid.UUID,
        nombre: str,
        apellido: str,
        documento: str,
        correo: str,
        telefono: str,
        fecha_registro: date,
        estado: str,
    ) -> Usuario | None:
        usuario = self.obtener_por_id(id_usuario)

        if usuario is None:
            return None

        usuario.nombre = nombre.strip()
        usuario.apellido = apellido.strip()
        usuario.documento = documento.strip()
        usuario.correo = correo.strip()
        usuario.telefono = telefono.strip()
        usuario.fecha_registro = fecha_registro
        usuario.estado = estado.strip()

        return usuario

    def eliminar(self, id_usuario: uuid.UUID) -> bool:
        usuario = self.obtener_por_id(id_usuario)

        if usuario is None:
            return False

        self.usuarios.remove(usuario)
        return True
