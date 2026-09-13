from sqlalchemy import text

from src.database.database import engine

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("Conexión exitosa con PostgreSQL/Neon")

except Exception as e:
    print("Error de conexión:")
    print(e)
