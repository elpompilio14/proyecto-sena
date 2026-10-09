"""Pestanas del menu que el admin puede ocultar desde /admin/paginas."""
from flask import g
from db import obtener_conexion

# grupo = menu desplegable donde aparece; rutas = paginas que se bloquean si se oculta
MENU = [
    ('Quiénes somos', [
        {'clave': 'historia', 'nombre': 'Historia', 'url': '/historia', 'rutas': ['/historia']},
        {'clave': 'institucion', 'nombre': 'Institución', 'url': '/institucion', 'rutas': ['/institucion']},
        {'clave': 'comunidad-educativa', 'nombre': 'Comunidad Educativa', 'url': '/comunidad-educativa', 'rutas': ['/comunidad-educativa']},
        {'clave': 'gobierno-escolar', 'nombre': 'Gobierno Escolar', 'url': '/gobierno-escolar', 'rutas': ['/gobierno-escolar']},
        {'clave': 'himno', 'nombre': 'Himno Escolar', 'url': '/himno', 'rutas': ['/himno']},
        {'clave': 'alianzas', 'nombre': 'Alianzas', 'url': '/alianzas', 'rutas': ['/alianzas']},
    ]),
    ('Conócenos', [
        {'clave': 'noticias', 'nombre': 'Noticias', 'url': '/noticias', 'rutas': ['/noticias']},
        {'clave': 'eventos', 'nombre': 'Eventos', 'url': '/eventos', 'rutas': ['/eventos']},
        {'clave': 'grupos-estudiantiles', 'nombre': 'Grupos y Semilleros', 'url': '/grupos-estudiantiles', 'rutas': ['/grupos-estudiantiles']},
        {'clave': 'deportes', 'nombre': 'Deportes', 'url': '/deportes', 'rutas': ['/deportes']},
        {'clave': 'campeonatos', 'nombre': 'Intercursos', 'url': '/campeonatos', 'rutas': ['/campeonatos']},
        {'clave': 'galeria', 'nombre': 'Galería', 'url': '/galeria', 'rutas': ['/galeria']},
        {'clave': 'mejores-puestos', 'nombre': 'Puestos de honor', 'url': '/mejores-puestos', 'rutas': ['/mejores-puestos']},
        {'clave': 'promociones', 'nombre': 'Promociones', 'url': '/promociones', 'rutas': ['/promociones', '/promocion']},
        {'clave': 'icfes', 'nombre': 'Mejores ICFES', 'url': '/icfes', 'rutas': ['/icfes']},
    ]),
    ('Media Técnica', [
        {'clave': 'articulado', 'nombre': 'Articulado', 'url': '/articulado', 'rutas': ['/articulado']},
        {'clave': 'investigacion', 'nombre': 'Investigación', 'url': '/investigacion', 'rutas': ['/investigacion']},
    ]),
]

CLAVES = [p['clave'] for _, paginas in MENU for p in paginas]


def paginas_ocultas():
    """Claves de las pestanas ocultas (se consulta una sola vez por request)."""
    if 'paginas_ocultas' not in g:
        try:
            with obtener_conexion() as conexion:
                with conexion.cursor() as cur:
                    cur.execute('SELECT clave FROM paginas_ocultas')
                    g.paginas_ocultas = {r['clave'] for r in cur.fetchall()}
        except Exception as err:
            print('No se pudieron cargar las paginas ocultas:', err)
            g.paginas_ocultas = set()
    return g.paginas_ocultas


def pagina_oculta_para(ruta):
    """Devuelve True si la ruta pertenece a una pestana oculta."""
    ocultas = paginas_ocultas()
    for _, paginas in MENU:
        for p in paginas:
            if p['clave'] in ocultas and any(ruta == r or ruta.startswith(r + '/') for r in p['rutas']):
                return True
    return False
