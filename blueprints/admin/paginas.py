from flask import render_template, request, redirect
from . import admin_bp
from db import obtener_conexion
from paginas import MENU, CLAVES, paginas_ocultas


@admin_bp.route('/paginas')
def paginas_index():
    return render_template(
        'admin/paginas.html', titulo='Admin · Pestañas del sitio',
        menu=MENU, ocultas=paginas_ocultas(), guardado=request.args.get('guardado'),
    )


@admin_bp.route('/paginas', methods=['POST'])
def paginas_guardar():
    visibles = set(request.form.getlist('visibles'))
    ocultas = [c for c in CLAVES if c not in visibles]
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM paginas_ocultas')
            for clave in ocultas:
                cur.execute('INSERT INTO paginas_ocultas (clave) VALUES (%s)', (clave,))
    return redirect('/admin/paginas?guardado=1')
