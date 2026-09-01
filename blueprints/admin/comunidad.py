from flask import render_template, request, redirect, abort, jsonify
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/comunidad-educativa')
def comunidad_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("""
                SELECT * FROM comunidad_educativa
                ORDER BY CASE categoria WHEN 'rectoria' THEN 1 WHEN 'coordinacion' THEN 2 ELSE 3 END, orden, nombre
            """)
            personas = cur.fetchall()
    return render_template('admin/comunidad.html', titulo='Admin · Comunidad Educativa', personas=personas)


@admin_bp.route('/comunidad-educativa', methods=['POST'])
def comunidad_crear():
    nombre = request.form.get('nombre')
    cargo = request.form.get('cargo') or None
    categoria = request.form.get('categoria') or 'docente'
    area = request.form.get('area') or None
    materia = request.form.get('materia') or None
    anios_experiencia = request.form.get('anios_experiencia') or None
    descripcion = request.form.get('descripcion') or None
    foto_url = guardar_archivo(request.files.get('imagen'))
    orden = request.form.get('orden') or 0
    nivel = request.form.get('nivel') or 'base'

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """INSERT INTO comunidad_educativa (nombre, cargo, categoria, area, materia, anios_experiencia, descripcion, foto_url, orden, nivel)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (nombre, cargo, categoria, area, materia, anios_experiencia, descripcion, foto_url, orden, nivel),
            )
    return redirect('/admin/comunidad-educativa')


@admin_bp.route('/comunidad-educativa/<int:id>/editar')
def comunidad_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM comunidad_educativa WHERE id = %s', (id,))
            persona = cur.fetchone()
    if not persona:
        abort(404)
    return render_template('admin/comunidad_editar.html', titulo='Admin · Editar persona', persona=persona)


@admin_bp.route('/comunidad-educativa/<int:id>/editar', methods=['POST'])
def comunidad_editar(id):
    nombre = request.form.get('nombre')
    cargo = request.form.get('cargo') or None
    categoria = request.form.get('categoria') or 'docente'
    area = request.form.get('area') or None
    materia = request.form.get('materia') or None
    anios_experiencia = request.form.get('anios_experiencia') or None
    descripcion = request.form.get('descripcion') or None
    foto_actual = request.form.get('foto_actual')
    foto_url = guardar_archivo(request.files.get('imagen')) or (foto_actual or None)
    orden = request.form.get('orden') or 0
    nivel = request.form.get('nivel') or 'base'

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """UPDATE comunidad_educativa
                   SET nombre = %s, cargo = %s, categoria = %s, area = %s, materia = %s,
                       anios_experiencia = %s, descripcion = %s, foto_url = %s, orden = %s, nivel = %s
                   WHERE id = %s""",
                (nombre, cargo, categoria, area, materia, anios_experiencia, descripcion, foto_url, orden, nivel, id),
            )
    return redirect('/admin/comunidad-educativa')


@admin_bp.route('/comunidad-educativa/<int:id>/eliminar', methods=['POST'])
def comunidad_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM comunidad_educativa WHERE id = %s', (id,))
    return redirect('/admin/comunidad-educativa')


@admin_bp.route('/comunidad-educativa/<int:id>/visibilidad', methods=['POST'])
def comunidad_toggle_visible(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('UPDATE comunidad_educativa SET visible = NOT visible WHERE id = %s RETURNING visible', (id,))
            resultado = cur.fetchone()
    return jsonify({'visible': resultado['visible']})
