from flask import render_template, request, redirect, abort, jsonify
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/media-tecnica')
def media_tecnica_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM media_tecnica_categorias ORDER BY orden, nombre')
            categorias = cur.fetchall()
    return render_template('admin/media_tecnica.html', titulo='Admin · Media Técnica', categorias=categorias)


@admin_bp.route('/media-tecnica', methods=['POST'])
def media_tecnica_crear():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion') or None
    orden = request.form.get('orden') or 0
    imagen_url = guardar_archivo(request.files.get('imagen'))
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'INSERT INTO media_tecnica_categorias (nombre, imagen_url, descripcion, orden) VALUES (%s, %s, %s, %s)',
                (nombre, imagen_url, descripcion, orden),
            )
    return redirect('/admin/media-tecnica')


@admin_bp.route('/media-tecnica/<int:id>/editar')
def media_tecnica_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM media_tecnica_categorias WHERE id = %s', (id,))
            categoria = cur.fetchone()
    if not categoria:
        abort(404)
    return render_template('admin/media_tecnica_editar.html', titulo='Admin · Editar categoría', categoria=categoria)


@admin_bp.route('/media-tecnica/<int:id>/editar', methods=['POST'])
def media_tecnica_editar(id):
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion') or None
    orden = request.form.get('orden') or 0
    imagen_actual = request.form.get('imagen_actual')
    imagen_url = guardar_archivo(request.files.get('imagen')) or (imagen_actual or None)
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE media_tecnica_categorias SET nombre = %s, imagen_url = %s, descripcion = %s, orden = %s WHERE id = %s',
                (nombre, imagen_url, descripcion, orden, id),
            )
    return redirect('/admin/media-tecnica')


@admin_bp.route('/media-tecnica/<int:id>/eliminar', methods=['POST'])
def media_tecnica_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM media_tecnica_categorias WHERE id = %s', (id,))
    return redirect('/admin/media-tecnica')


@admin_bp.route('/media-tecnica/<int:id>/visibilidad', methods=['POST'])
def media_tecnica_toggle_visible(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('UPDATE media_tecnica_categorias SET visible = NOT visible WHERE id = %s RETURNING visible', (id,))
            resultado = cur.fetchone()
    return jsonify({'visible': resultado['visible']})
