import os
import psycopg
from psycopg.rows import dict_row


def obtener_conexion():
    """Abre una conexión nueva a PostgreSQL. Cada request pide la suya y la cierra al terminar."""
    return psycopg.connect(
        host=os.environ.get('PGHOST'),
        port=os.environ.get('PGPORT'),
        user=os.environ.get('PGUSER'),
        password=os.environ.get('PGPASSWORD'),
        dbname=os.environ.get('PGDATABASE'),
        row_factory=dict_row,
        autocommit=True,
    )
