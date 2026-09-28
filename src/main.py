import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.autores import autores_router
from src.api.categorias import categorias_router
from src.api.editoriales import editoriales_router
from src.api.ejemplares import ejemplares_router
from src.api.libros import libros_router
from src.api.multas import multas_router
from src.api.prestamos import prestamos_router
from src.api.usuarios import usuarios_router

app = FastAPI(
    title="API Biblioteca — Programación de Software 2026-2",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def raiz():
    """Verifica que la API esté funcionando."""
    return {"mensaje": "API en marcha"}


app.include_router(usuarios_router)
app.include_router(autores_router)
app.include_router(categorias_router)
app.include_router(editoriales_router)
app.include_router(ejemplares_router)
app.include_router(libros_router)
app.include_router(prestamos_router)
app.include_router(multas_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
