from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/deportes')
def deportes_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM deportes ORDER BY nombre')
            deportes = cur.fetchall()
    return render_template('admin/deportes.html', titulo='Admin · Deportes', deportes=deportes)


@admin_bp.route('/deportes', methods=['POST'])
def deportes_crear():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion') or None
    imagen_url = guardar_archivo(request.files.get('imagen'))
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'INSERT INTO deportes (nombre, imagen_url, descripcion) VALUES (%s, %s, %s)',
                (nombre, imagen_url, descripcion),
            )
    return redirect('/admin/deportes')


@admin_bp.route('/deportes/<int:id>/editar')
def deportes_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM deportes WHERE id = %s', (id,))
            deporte = cur.fetchone()
    if not deporte:
        abort(404)
    return render_template('admin/deportes_editar.html', titulo='Admin · Editar deporte', deporte=deporte)


@admin_bp.route('/deportes/<int:id>/editar', methods=['POST'])
def deportes_editar(id):
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion') or None
    imagen_actual = request.form.get('imagen_actual')
    imagen_url = guardar_archivo(request.files.get('imagen')) or (imagen_actual or None)
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE deportes SET nombre = %s, imagen_url = %s, descripcion = %s WHERE id = %s',
                (nombre, imagen_url, descripcion, id),
            )
    return redirect('/admin/deportes')


@admin_bp.route('/deportes/<int:id>/eliminar', methods=['POST'])
def deportes_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM deportes WHERE id = %s', (id,))
    return redirect('/admin/deportes')
