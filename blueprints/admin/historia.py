from flask import render_template, request, redirect, abort, jsonify
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/historia')
def historia_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT historia, historia_foto_url FROM institucion_info ORDER BY id LIMIT 1')
            intro = cur.fetchone() or {}
            cur.execute('SELECT * FROM historia_bloques ORDER BY orden, id')
            bloques = cur.fetchall()
    return render_template('admin/historia.html', titulo='Admin · Historia', intro=intro, bloques=bloques)


@admin_bp.route('/historia/intro', methods=['POST'])
def historia_actualizar_intro():
    foto_url = guardar_archivo(request.files.get('foto')) or (request.form.get('foto_actual') or None)
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """UPDATE institucion_info SET historia = %s, historia_foto_url = %s
                   WHERE id = (SELECT id FROM institucion_info ORDER BY id LIMIT 1)""",
                (request.form.get('texto') or None, foto_url),
            )
    return redirect('/admin/historia')


def _datos_bloque(f):
    foto_url = guardar_archivo(request.files.get('foto')) or (f.get('foto_actual') or None)
    return (f.get('titulo') or None, f.get('texto') or None, foto_url, f.get('foto_pie') or None, f.get('orden') or 0)


@admin_bp.route('/historia', methods=['POST'])
def historia_crear_bloque():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'INSERT INTO historia_bloques (titulo, texto, foto_url, foto_pie, orden) VALUES (%s, %s, %s, %s, %s)',
                _datos_bloque(request.form),
            )
    return redirect('/admin/historia')


@admin_bp.route('/historia/<int:id>/editar')
def historia_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM historia_bloques WHERE id = %s', (id,))
            bloque = cur.fetchone()
    if not bloque:
        abort(404)
    return render_template('admin/historia_editar.html', titulo='Admin · Editar bloque de historia', bloque=bloque)


@admin_bp.route('/historia/<int:id>/editar', methods=['POST'])
def historia_editar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE historia_bloques SET titulo = %s, texto = %s, foto_url = %s, foto_pie = %s, orden = %s WHERE id = %s',
                _datos_bloque(request.form) + (id,),
            )
    return redirect('/admin/historia')


@admin_bp.route('/historia/<int:id>/eliminar', methods=['POST'])
def historia_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM historia_bloques WHERE id = %s', (id,))
    return redirect('/admin/historia')


@admin_bp.route('/historia/<int:id>/visibilidad', methods=['POST'])
def historia_toggle_visible(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('UPDATE historia_bloques SET visible = NOT visible WHERE id = %s RETURNING visible', (id,))
            resultado = cur.fetchone()
    return jsonify({'visible': resultado['visible']})
