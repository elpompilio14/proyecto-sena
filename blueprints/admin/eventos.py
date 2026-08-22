from flask import render_template, request, redirect, session, abort
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/eventos')
def eventos_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM eventos ORDER BY fecha DESC')
            eventos = cur.fetchall()
    return render_template('admin/eventos.html', titulo='Admin · Eventos', eventos=eventos)


@admin_bp.route('/eventos', methods=['POST'])
def eventos_crear():
    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    fecha = request.form.get('fecha')
    imagen_url = guardar_archivo(request.files.get('imagen'))

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """INSERT INTO eventos (titulo, descripcion, fecha, imagen_url, creado_por)
                   VALUES (%s, %s, %s, %s, %s)""",
                (titulo, descripcion, fecha, imagen_url, session['usuario']['id']),
            )
    return redirect('/admin/eventos')


@admin_bp.route('/eventos/<int:id>/editar')
def eventos_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM eventos WHERE id = %s', (id,))
            evento = cur.fetchone()
    if not evento:
        abort(404)
    return render_template('admin/eventos_editar.html', titulo='Admin · Editar evento', evento=evento)


@admin_bp.route('/eventos/<int:id>/editar', methods=['POST'])
def eventos_editar(id):
    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    fecha = request.form.get('fecha')
    imagen_actual = request.form.get('imagen_actual')
    imagen_url = guardar_archivo(request.files.get('imagen')) or (imagen_actual or None)

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE eventos SET titulo = %s, descripcion = %s, fecha = %s, imagen_url = %s WHERE id = %s',
                (titulo, descripcion, fecha, imagen_url, id),
            )
    return redirect('/admin/eventos')


@admin_bp.route('/eventos/<int:id>/eliminar', methods=['POST'])
def eventos_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM eventos WHERE id = %s', (id,))
    return redirect('/admin/eventos')
