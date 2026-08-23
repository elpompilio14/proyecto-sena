from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/equipo-desarrollo')
def equipo_desarrollo_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM equipo_desarrollo ORDER BY orden, nombre')
            miembros = cur.fetchall()
    return render_template('admin/equipo_desarrollo.html', titulo='Admin · Equipo de Desarrollo', miembros=miembros)


@admin_bp.route('/equipo-desarrollo', methods=['POST'])
def equipo_desarrollo_crear():
    nombre = request.form.get('nombre')
    rol = request.form.get('rol') or None
    foto_url = guardar_archivo(request.files.get('imagen'))
    orden = request.form.get('orden') or 0

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'INSERT INTO equipo_desarrollo (nombre, rol, foto_url, orden) VALUES (%s, %s, %s, %s)',
                (nombre, rol, foto_url, orden),
            )
    return redirect('/admin/equipo-desarrollo')


@admin_bp.route('/equipo-desarrollo/<int:id>/editar')
def equipo_desarrollo_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM equipo_desarrollo WHERE id = %s', (id,))
            miembro = cur.fetchone()
    if not miembro:
        abort(404)
    return render_template('admin/equipo_desarrollo_editar.html', titulo='Admin · Editar miembro', miembro=miembro)


@admin_bp.route('/equipo-desarrollo/<int:id>/editar', methods=['POST'])
def equipo_desarrollo_editar(id):
    nombre = request.form.get('nombre')
    rol = request.form.get('rol') or None
    foto_actual = request.form.get('foto_actual')
    foto_url = guardar_archivo(request.files.get('imagen')) or (foto_actual or None)
    orden = request.form.get('orden') or 0

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE equipo_desarrollo SET nombre = %s, rol = %s, foto_url = %s, orden = %s WHERE id = %s',
                (nombre, rol, foto_url, orden, id),
            )
    return redirect('/admin/equipo-desarrollo')


@admin_bp.route('/equipo-desarrollo/<int:id>/eliminar', methods=['POST'])
def equipo_desarrollo_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM equipo_desarrollo WHERE id = %s', (id,))
    return redirect('/admin/equipo-desarrollo')
