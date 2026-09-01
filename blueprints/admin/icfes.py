from flask import render_template, request, redirect, abort, jsonify
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/icfes')
def icfes_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM icfes_resultados ORDER BY anio DESC, puntaje DESC')
            resultados = cur.fetchall()
    return render_template('admin/icfes.html', titulo='Admin · Mejores ICFES', resultados=resultados)


@admin_bp.route('/icfes', methods=['POST'])
def icfes_crear():
    estudiante_nombre = request.form.get('estudiante_nombre')
    puntaje = request.form.get('puntaje')
    anio = request.form.get('anio')
    descripcion = request.form.get('descripcion') or None
    foto_url = guardar_archivo(request.files.get('imagen'))

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """INSERT INTO icfes_resultados (estudiante_nombre, puntaje, anio, foto_url, descripcion)
                   VALUES (%s, %s, %s, %s, %s)""",
                (estudiante_nombre, puntaje, anio, foto_url, descripcion),
            )
    return redirect('/admin/icfes')


@admin_bp.route('/icfes/<int:id>/editar')
def icfes_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM icfes_resultados WHERE id = %s', (id,))
            resultado = cur.fetchone()
    if not resultado:
        abort(404)
    return render_template('admin/icfes_editar.html', titulo='Admin · Editar resultado ICFES', resultado=resultado)


@admin_bp.route('/icfes/<int:id>/editar', methods=['POST'])
def icfes_editar(id):
    estudiante_nombre = request.form.get('estudiante_nombre')
    puntaje = request.form.get('puntaje')
    anio = request.form.get('anio')
    descripcion = request.form.get('descripcion') or None
    foto_actual = request.form.get('foto_actual')
    foto_url = guardar_archivo(request.files.get('imagen')) or (foto_actual or None)

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """UPDATE icfes_resultados SET estudiante_nombre = %s, puntaje = %s, anio = %s, foto_url = %s, descripcion = %s
                   WHERE id = %s""",
                (estudiante_nombre, puntaje, anio, foto_url, descripcion, id),
            )
    return redirect('/admin/icfes')


@admin_bp.route('/icfes/<int:id>/eliminar', methods=['POST'])
def icfes_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM icfes_resultados WHERE id = %s', (id,))
    return redirect('/admin/icfes')


@admin_bp.route('/icfes/<int:id>/visibilidad', methods=['POST'])
def icfes_toggle_visible(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('UPDATE icfes_resultados SET visible = NOT visible WHERE id = %s RETURNING visible', (id,))
            resultado = cur.fetchone()
    return jsonify({'visible': resultado['visible']})
