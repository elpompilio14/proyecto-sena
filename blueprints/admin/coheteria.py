from flask import render_template, request, redirect, abort, jsonify
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/coheteria')
def coheteria_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM coheteria ORDER BY orden, nombre')
            miembros = cur.fetchall()
            cur.execute('SELECT coheteria_texto, coheteria_portada_url FROM institucion_info ORDER BY id LIMIT 1')
            info = cur.fetchone()
    return render_template(
        'admin/coheteria.html',
        titulo='Admin · Cohetería',
        miembros=miembros,
        infoTexto=info['coheteria_texto'] if info else '',
        infoPortada=info['coheteria_portada_url'] if info else None,
    )


@admin_bp.route('/coheteria/info', methods=['POST'])
def coheteria_actualizar_info():
    texto = request.form.get('texto')
    portada_actual = request.form.get('portada_actual')
    portada_url = guardar_archivo(request.files.get('portada')) or (portada_actual or None)
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE institucion_info SET coheteria_texto = %s, coheteria_portada_url = %s WHERE id = (SELECT id FROM institucion_info ORDER BY id LIMIT 1)',
                (texto or None, portada_url),
            )
    return redirect('/admin/coheteria')


@admin_bp.route('/coheteria', methods=['POST'])
def coheteria_crear():
    nombre = request.form.get('nombre')
    rol = request.form.get('rol') or None
    foto_url = guardar_archivo(request.files.get('imagen'))
    orden = request.form.get('orden') or 0
    nivel = request.form.get('nivel') or 'base'

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'INSERT INTO coheteria (nombre, rol, foto_url, orden, nivel) VALUES (%s, %s, %s, %s, %s)',
                (nombre, rol, foto_url, orden, nivel),
            )
    return redirect('/admin/coheteria')


@admin_bp.route('/coheteria/<int:id>/editar')
def coheteria_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM coheteria WHERE id = %s', (id,))
            miembro = cur.fetchone()
    if not miembro:
        abort(404)
    return render_template('admin/coheteria_editar.html', titulo='Admin · Editar miembro', miembro=miembro)


@admin_bp.route('/coheteria/<int:id>/editar', methods=['POST'])
def coheteria_editar(id):
    nombre = request.form.get('nombre')
    rol = request.form.get('rol') or None
    foto_actual = request.form.get('foto_actual')
    foto_url = guardar_archivo(request.files.get('imagen')) or (foto_actual or None)
    orden = request.form.get('orden') or 0
    nivel = request.form.get('nivel') or 'base'

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE coheteria SET nombre = %s, rol = %s, foto_url = %s, orden = %s, nivel = %s WHERE id = %s',
                (nombre, rol, foto_url, orden, nivel, id),
            )
    return redirect('/admin/coheteria')


@admin_bp.route('/coheteria/<int:id>/eliminar', methods=['POST'])
def coheteria_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM coheteria WHERE id = %s', (id,))
    return redirect('/admin/coheteria')


@admin_bp.route('/coheteria/<int:id>/visibilidad', methods=['POST'])
def coheteria_toggle_visible(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('UPDATE coheteria SET visible = NOT visible WHERE id = %s RETURNING visible', (id,))
            resultado = cur.fetchone()
    return jsonify({'visible': resultado['visible']})
