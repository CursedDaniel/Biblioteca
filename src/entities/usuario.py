from datetime import date


class Usuario:
    def __init__(
        self,
        id_usuario: int,
        nombre: str,
        apellido: str,
        documento: str,
        correo: str,
        telefono: str,
        fecha_registro: str,
        estado: str,
    ):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.fecha_registro = fecha_registro
        self.estado = estado
