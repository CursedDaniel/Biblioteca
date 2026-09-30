import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.api.routers.autor import router as autores_router
from src.api.routers.categoria import router as categorias_router
from src.api.routers.editorial import router as editoriales_router
from src.api.routers.ejemplar import router as ejemplares_router
from src.api.routers.libro import router as libros_router
from src.api.routers.multa import router as multas_router
from src.api.routers.prestamo import router as prestamos_router
from src.api.routers.usuario import router as usuarios_router

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


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
