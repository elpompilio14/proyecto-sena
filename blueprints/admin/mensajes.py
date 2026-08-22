from flask import render_template, redirect
from . import admin_bp
from db import obtener_conexion


@admin_bp.route('/mensajes')
def mensajes_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM mensajes_contacto ORDER BY creado_en DESC')
            mensajes = cur.fetchall()
    return render_template('admin/mensajes.html', titulo='Admin · Mensajes', mensajes=mensajes)


@admin_bp.route('/mensajes/<int:id>/leido', methods=['POST'])
def mensajes_marcar_leido(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('UPDATE mensajes_contacto SET leido = TRUE WHERE id = %s', (id,))
    return redirect('/admin/mensajes')


@admin_bp.route('/mensajes/<int:id>/eliminar', methods=['POST'])
def mensajes_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM mensajes_contacto WHERE id = %s', (id,))
    return redirect('/admin/mensajes')
