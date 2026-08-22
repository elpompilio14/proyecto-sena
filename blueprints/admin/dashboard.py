from flask import render_template
from . import admin_bp
from db import obtener_conexion


@admin_bp.route('/', strict_slashes=False)
def dashboard_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT COUNT(*) AS total FROM mensajes_contacto WHERE leido = FALSE')
            mensajes_no_leidos = cur.fetchone()['total']

    return render_template('admin/dashboard.html', titulo='Panel admin', mensajesNoLeidos=mensajes_no_leidos)
