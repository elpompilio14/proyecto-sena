from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion


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
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('INSERT INTO deportes (nombre) VALUES (%s)', (nombre,))
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
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('UPDATE deportes SET nombre = %s WHERE id = %s', (nombre, id))
    return redirect('/admin/deportes')


@admin_bp.route('/deportes/<int:id>/eliminar', methods=['POST'])
def deportes_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM deportes WHERE id = %s', (id,))
    return redirect('/admin/deportes')
