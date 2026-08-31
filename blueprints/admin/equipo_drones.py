from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/equipo-drones')
def equipo_drones_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM equipo_drones ORDER BY orden, nombre')
            miembros = cur.fetchall()
    return render_template('admin/equipo_drones.html', titulo='Admin · Equipo de Drones', miembros=miembros)


@admin_bp.route('/equipo-drones', methods=['POST'])
def equipo_drones_crear():
    nombre = request.form.get('nombre')
    rol = request.form.get('rol') or None
    foto_url = guardar_archivo(request.files.get('imagen'))
    orden = request.form.get('orden') or 0
    nivel = request.form.get('nivel') or 'base'

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'INSERT INTO equipo_drones (nombre, rol, foto_url, orden, nivel) VALUES (%s, %s, %s, %s, %s)',
                (nombre, rol, foto_url, orden, nivel),
            )
    return redirect('/admin/equipo-drones')


@admin_bp.route('/equipo-drones/<int:id>/editar')
def equipo_drones_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM equipo_drones WHERE id = %s', (id,))
            miembro = cur.fetchone()
    if not miembro:
        abort(404)
    return render_template('admin/equipo_drones_editar.html', titulo='Admin · Editar miembro', miembro=miembro)


@admin_bp.route('/equipo-drones/<int:id>/editar', methods=['POST'])
def equipo_drones_editar(id):
    nombre = request.form.get('nombre')
    rol = request.form.get('rol') or None
    foto_actual = request.form.get('foto_actual')
    foto_url = guardar_archivo(request.files.get('imagen')) or (foto_actual or None)
    orden = request.form.get('orden') or 0
    nivel = request.form.get('nivel') or 'base'

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE equipo_drones SET nombre = %s, rol = %s, foto_url = %s, orden = %s, nivel = %s WHERE id = %s',
                (nombre, rol, foto_url, orden, nivel, id),
            )
    return redirect('/admin/equipo-drones')


@admin_bp.route('/equipo-drones/<int:id>/eliminar', methods=['POST'])
def equipo_drones_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM equipo_drones WHERE id = %s', (id,))
    return redirect('/admin/equipo-drones')
