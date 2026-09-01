from flask import render_template, request, redirect, abort, jsonify
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/equipos')
def equipos_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("""
                SELECT equipos.*, deportes.nombre AS deporte_nombre
                FROM equipos
                JOIN deportes ON deportes.id = equipos.deporte_id
                ORDER BY deportes.nombre, equipos.nombre
            """)
            equipos = cur.fetchall()
            cur.execute('SELECT * FROM deportes ORDER BY nombre')
            deportes = cur.fetchall()

    return render_template('admin/equipos.html', titulo='Admin · Equipos', equipos=equipos, deportes=deportes)


@admin_bp.route('/equipos', methods=['POST'])
def equipos_crear():
    nombre = request.form.get('nombre')
    deporte_id = request.form.get('deporte_id')
    categoria = request.form.get('categoria') or None
    entrenador = request.form.get('entrenador') or None
    descripcion = request.form.get('descripcion') or None
    foto_url = guardar_archivo(request.files.get('imagen'))

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """INSERT INTO equipos (nombre, deporte_id, categoria, entrenador, foto_url, descripcion)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (nombre, deporte_id, categoria, entrenador, foto_url, descripcion),
            )
    return redirect('/admin/equipos')


@admin_bp.route('/equipos/<int:id>/editar')
def equipos_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM equipos WHERE id = %s', (id,))
            equipo = cur.fetchone()
            if not equipo:
                abort(404)
            cur.execute('SELECT * FROM deportes ORDER BY nombre')
            deportes = cur.fetchall()

    return render_template('admin/equipos_editar.html', titulo='Admin · Editar equipo', equipo=equipo, deportes=deportes)


@admin_bp.route('/equipos/<int:id>/editar', methods=['POST'])
def equipos_editar(id):
    nombre = request.form.get('nombre')
    deporte_id = request.form.get('deporte_id')
    categoria = request.form.get('categoria') or None
    entrenador = request.form.get('entrenador') or None
    descripcion = request.form.get('descripcion') or None
    foto_actual = request.form.get('foto_actual')
    foto_url = guardar_archivo(request.files.get('imagen')) or (foto_actual or None)

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """UPDATE equipos SET nombre = %s, deporte_id = %s, categoria = %s, entrenador = %s, foto_url = %s, descripcion = %s
                   WHERE id = %s""",
                (nombre, deporte_id, categoria, entrenador, foto_url, descripcion, id),
            )
    return redirect('/admin/equipos')


@admin_bp.route('/equipos/<int:id>/eliminar', methods=['POST'])
def equipos_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM equipos WHERE id = %s', (id,))
    return redirect('/admin/equipos')


@admin_bp.route('/equipos/<int:id>/visibilidad', methods=['POST'])
def equipos_toggle_visible(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('UPDATE equipos SET visible = NOT visible WHERE id = %s RETURNING visible', (id,))
            resultado = cur.fetchone()
    return jsonify({'visible': resultado['visible']})
