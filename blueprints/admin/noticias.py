from flask import render_template, request, redirect, session, abort, jsonify
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/noticias')
def noticias_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM noticias ORDER BY fecha DESC')
            noticias = cur.fetchall()
    return render_template('admin/noticias.html', titulo='Admin · Noticias', noticias=noticias)


@admin_bp.route('/noticias', methods=['POST'])
def noticias_crear():
    titulo = request.form.get('titulo')
    contenido = request.form.get('contenido')
    fecha = request.form.get('fecha')
    imagen_url = guardar_archivo(request.files.get('imagen'))

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """INSERT INTO noticias (titulo, contenido, fecha, imagen_url, creado_por)
                   VALUES (%s, %s, %s, %s, %s)""",
                (titulo, contenido, fecha, imagen_url, session['usuario']['id']),
            )
    return redirect('/admin/noticias')


@admin_bp.route('/noticias/<int:id>/editar')
def noticias_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM noticias WHERE id = %s', (id,))
            noticia = cur.fetchone()
    if not noticia:
        abort(404)
    return render_template('admin/noticias_editar.html', titulo='Admin · Editar noticia', noticia=noticia)


@admin_bp.route('/noticias/<int:id>/editar', methods=['POST'])
def noticias_editar(id):
    titulo = request.form.get('titulo')
    contenido = request.form.get('contenido')
    fecha = request.form.get('fecha')
    imagen_actual = request.form.get('imagen_actual')
    imagen_url = guardar_archivo(request.files.get('imagen')) or (imagen_actual or None)

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE noticias SET titulo = %s, contenido = %s, fecha = %s, imagen_url = %s WHERE id = %s',
                (titulo, contenido, fecha, imagen_url, id),
            )
    return redirect('/admin/noticias')


@admin_bp.route('/noticias/<int:id>/eliminar', methods=['POST'])
def noticias_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM noticias WHERE id = %s', (id,))
    return redirect('/admin/noticias')


@admin_bp.route('/noticias/<int:id>/visibilidad', methods=['POST'])
def noticias_toggle_visible(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('UPDATE noticias SET visible = NOT visible WHERE id = %s RETURNING visible', (id,))
            resultado = cur.fetchone()
    return jsonify({'visible': resultado['visible']})
