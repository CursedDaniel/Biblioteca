import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.autores import autores_router
from src.api.routers.categorias import categorias_router
from src.api.routers.editoriales import editoriales_router
from src.api.routers.ejemplares import ejemplares_router
from src.api.routers.libros import libros_router
from src.api.routers.multas import multas_router
from src.api.routers.prestamos import prestamos_router
from src.api.routers.usuarios import usuarios_router

# Creamos la aplicación FastAPI.
app = FastAPI(
    title="API Biblioteca — Programación de Software 2026-2",
    version="1.0.0",
)


# Configuración de CORS.
app.add_middleware(
    CORSMiddleware,
    # Durante desarrollo permitimos cualquier origen.
    allow_origins=["*"],
    # Permite solicitudes que utilicen credenciales.
    allow_credentials=True,
    # Permite los métodos HTTP.
    allow_methods=["*"],
    # Permite las cabeceras HTTP.
    allow_headers=["*"],
)


# Endpoint básico para comprobar que la API está funcionando.
@app.get("/")
def raiz():
    return {"mensaje": "API en marcha"}


# Registramos los routers de cada entidad.
app.include_router(usuarios_router)
app.include_router(autores_router)
app.include_router(categorias_router)
app.include_router(editoriales_router)
app.include_router(ejemplares_router)
app.include_router(libros_router)
app.include_router(prestamos_router)
app.include_router(multas_router)


# Permite ejecutar la API directamente con:
# python -m src.main
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
