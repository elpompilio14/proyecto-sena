import os
import time
import random
from werkzeug.utils import secure_filename

CARPETA_IMAGENES = os.path.join(os.path.dirname(__file__), 'static', 'images')

TIPOS_IMAGEN = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
TIPOS_IMAGEN_Y_VIDEO = TIPOS_IMAGEN + ['.mp4', '.webm', '.mov', '.ogg']


def _extension(nombre_archivo):
    return os.path.splitext(nombre_archivo)[1].lower()


def guardar_archivo(file_storage, tipos_permitidos=TIPOS_IMAGEN):
    """Guarda un archivo subido con un nombre unico y devuelve la URL (/images/xxx.ext),
    igual que hacia multer. Si el archivo no cumple la extension permitida, devuelve None."""
    if not file_storage or not file_storage.filename:
        return None

    extension = _extension(file_storage.filename)
    if extension not in tipos_permitidos:
        raise ValueError('Tipo de archivo no permitido: ' + extension)

    nombre_unico = f"{int(time.time() * 1000)}-{random.randint(0, 999999999)}{extension}"
    os.makedirs(CARPETA_IMAGENES, exist_ok=True)
    file_storage.save(os.path.join(CARPETA_IMAGENES, secure_filename(nombre_unico)))

    return f'/images/{nombre_unico}'
