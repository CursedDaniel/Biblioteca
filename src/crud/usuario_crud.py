import uuid

from datetime import date

from sqlalchemy.orm import Session

from src.entities.usuario import Usuario


class UsuarioCrud:
    def __init__(self, session: Session):
        self.session = session

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
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            documento=documento.strip(),
            correo=correo.strip(),
            telefono=telefono.strip(),
            fecha_registro=fecha_registro,
            estado=estado.strip(),
        )

        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)

        return usuario

    def obtener_por_id(
        self,
        id_usuario: uuid.UUID,
    ) -> Usuario | None:
        return self.session.get(Usuario, id_usuario)

    def obtener_por_documento(
        self,
        documento: str,
    ) -> Usuario | None:
        documento_normalizado = documento.strip()

        return (
            self.session.query(Usuario)
            .filter(Usuario.documento == documento_normalizado)
            .first()
        )

    def obtener_todos(self) -> list[Usuario]:
        return self.session.query(Usuario).all()

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

        self.session.commit()
        self.session.refresh(usuario)

        return usuario

    def eliminar(self, id_usuario: uuid.UUID) -> bool:
        usuario = self.obtener_por_id(id_usuario)

        if usuario is None:
            return False

        self.session.delete(usuario)
        self.session.commit()

        return True
