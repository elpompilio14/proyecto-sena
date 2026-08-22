import random


def generar_codigo():
    """Genera un codigo numerico de 6 digitos como texto (con ceros a la izquierda si hace falta)."""
    return str(random.randint(0, 999999)).zfill(6)
