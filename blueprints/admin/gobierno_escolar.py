from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/gobierno-escolar')
def gobierno_escolar_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM gobierno_escolar ORDER BY orden, nombre')
            miembros = cur.fetchall()
    return render_template('admin/gobierno_escolar.html', titulo='Admin · Gobierno Escolar', miembros=miembros)


@admin_bp.route('/gobierno-escolar', methods=['POST'])
def gobierno_escolar_crear():
    nombre = request.form.get('nombre')
    rol = request.form.get('rol') or None
    foto_url = guardar_archivo(request.files.get('imagen'))
    orden = request.form.get('orden') or 0

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'INSERT INTO gobierno_escolar (nombre, rol, foto_url, orden) VALUES (%s, %s, %s, %s)',
                (nombre, rol, foto_url, orden),
            )
    return redirect('/admin/gobierno-escolar')


@admin_bp.route('/gobierno-escolar/<int:id>/editar')
def gobierno_escolar_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM gobierno_escolar WHERE id = %s', (id,))
            miembro = cur.fetchone()
    if not miembro:
        abort(404)
    return render_template('admin/gobierno_escolar_editar.html', titulo='Admin · Editar miembro', miembro=miembro)


@admin_bp.route('/gobierno-escolar/<int:id>/editar', methods=['POST'])
def gobierno_escolar_editar(id):
    nombre = request.form.get('nombre')
    rol = request.form.get('rol') or None
    foto_actual = request.form.get('foto_actual')
    foto_url = guardar_archivo(request.files.get('imagen')) or (foto_actual or None)
    orden = request.form.get('orden') or 0

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE gobierno_escolar SET nombre = %s, rol = %s, foto_url = %s, orden = %s WHERE id = %s',
                (nombre, rol, foto_url, orden, id),
            )
    return redirect('/admin/gobierno-escolar')


@admin_bp.route('/gobierno-escolar/<int:id>/eliminar', methods=['POST'])
def gobierno_escolar_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM gobierno_escolar WHERE id = %s', (id,))
    return redirect('/admin/gobierno-escolar')
