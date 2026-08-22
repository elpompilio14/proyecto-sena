from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/alianzas')
def alianzas_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM alianzas ORDER BY nombre')
            alianzas = cur.fetchall()
    return render_template('admin/alianzas.html', titulo='Admin · Alianzas', alianzas=alianzas)


@admin_bp.route('/alianzas', methods=['POST'])
def alianzas_crear():
    nombre = request.form.get('nombre')
    link_url = request.form.get('link_url') or None
    logo_url = guardar_archivo(request.files.get('imagen'))

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'INSERT INTO alianzas (nombre, logo_url, link_url) VALUES (%s, %s, %s)',
                (nombre, logo_url, link_url),
            )
    return redirect('/admin/alianzas')


@admin_bp.route('/alianzas/<int:id>/editar')
def alianzas_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM alianzas WHERE id = %s', (id,))
            alianza = cur.fetchone()
    if not alianza:
        abort(404)
    return render_template('admin/alianzas_editar.html', titulo='Admin · Editar alianza', alianza=alianza)


@admin_bp.route('/alianzas/<int:id>/editar', methods=['POST'])
def alianzas_editar(id):
    nombre = request.form.get('nombre')
    link_url = request.form.get('link_url') or None
    logo_actual = request.form.get('logo_actual')
    logo_url = guardar_archivo(request.files.get('imagen')) or (logo_actual or None)

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE alianzas SET nombre = %s, logo_url = %s, link_url = %s WHERE id = %s',
                (nombre, logo_url, link_url, id),
            )
    return redirect('/admin/alianzas')


@admin_bp.route('/alianzas/<int:id>/eliminar', methods=['POST'])
def alianzas_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM alianzas WHERE id = %s', (id,))
    return redirect('/admin/alianzas')
