from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion


@admin_bp.route('/grados')
def grados_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM grados ORDER BY nivel, nombre')
            grados = cur.fetchall()
    return render_template('admin/grados.html', titulo='Admin · Grados', grados=grados)


@admin_bp.route('/grados', methods=['POST'])
def grados_crear():
    nombre = request.form.get('nombre')
    nivel = request.form.get('nivel')
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('INSERT INTO grados (nombre, nivel) VALUES (%s, %s)', (nombre, nivel))
    return redirect('/admin/grados')


@admin_bp.route('/grados/<int:id>/editar')
def grados_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM grados WHERE id = %s', (id,))
            grado = cur.fetchone()
    if not grado:
        abort(404)
    return render_template('admin/grados_editar.html', titulo='Admin · Editar grado', grado=grado)


@admin_bp.route('/grados/<int:id>/editar', methods=['POST'])
def grados_editar(id):
    nombre = request.form.get('nombre')
    nivel = request.form.get('nivel')
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('UPDATE grados SET nombre = %s, nivel = %s WHERE id = %s', (nombre, nivel, id))
    return redirect('/admin/grados')


@admin_bp.route('/grados/<int:id>/eliminar', methods=['POST'])
def grados_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM grados WHERE id = %s', (id,))
    return redirect('/admin/grados')
