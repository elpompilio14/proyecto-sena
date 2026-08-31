from flask import Blueprint, redirect, session

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.before_request
def _requerir_admin():
    usuario = session.get('usuario')
    if not usuario or usuario.get('rol') != 'admin':
        return redirect('/login')


from . import (  # noqa: E402  (import al final para evitar import circular con admin_bp)
    dashboard,
    institucion,
    eventos,
    noticias,
    fotos,
    equipos,
    campeonatos,
    resultados,
    estudiantes,
    mejores_puestos,
    mensajes,
    grados,
    deportes,
    media_tecnica,
    grupos_estudiantiles,
    comunidad,
    icfes,
    alianzas,
    gobierno_escolar,
    equipo_desarrollo,
    comite_ecologico,
    equipo_drones,
    coheteria,
)
