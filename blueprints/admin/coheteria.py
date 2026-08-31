from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/coheteria')
def coheteria_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM coheteria ORDER BY orden, nombre')
            miembros = cur.fetchall()
    return render_template('admin/coheteria.html', titulo='Admin · Cohetería', miembros=miembros)


@admin_bp.route('/coheteria', methods=['POST'])
def coheteria_crear():
    nombre = request.form.get('nombre')
    rol = request.form.get('rol') or None
    foto_url = guardar_archivo(request.files.get('imagen'))
    orden = request.form.get('orden') or 0
    nivel = request.form.get('nivel') or 'base'

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'INSERT INTO coheteria (nombre, rol, foto_url, orden, nivel) VALUES (%s, %s, %s, %s, %s)',
                (nombre, rol, foto_url, orden, nivel),
            )
    return redirect('/admin/coheteria')


@admin_bp.route('/coheteria/<int:id>/editar')
def coheteria_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM coheteria WHERE id = %s', (id,))
            miembro = cur.fetchone()
    if not miembro:
        abort(404)
    return render_template('admin/coheteria_editar.html', titulo='Admin · Editar miembro', miembro=miembro)


@admin_bp.route('/coheteria/<int:id>/editar', methods=['POST'])
def coheteria_editar(id):
    nombre = request.form.get('nombre')
    rol = request.form.get('rol') or None
    foto_actual = request.form.get('foto_actual')
    foto_url = guardar_archivo(request.files.get('imagen')) or (foto_actual or None)
    orden = request.form.get('orden') or 0
    nivel = request.form.get('nivel') or 'base'

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE coheteria SET nombre = %s, rol = %s, foto_url = %s, orden = %s, nivel = %s WHERE id = %s',
                (nombre, rol, foto_url, orden, nivel, id),
            )
    return redirect('/admin/coheteria')


@admin_bp.route('/coheteria/<int:id>/eliminar', methods=['POST'])
def coheteria_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM coheteria WHERE id = %s', (id,))
    return redirect('/admin/coheteria')
