from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion


@admin_bp.route('/campeonatos')
def campeonatos_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("""
                SELECT campeonatos.*, deportes.nombre AS deporte_nombre
                FROM campeonatos
                JOIN deportes ON deportes.id = campeonatos.deporte_id
                ORDER BY campeonatos.fecha_inicio DESC
            """)
            campeonatos = cur.fetchall()
            cur.execute('SELECT * FROM deportes ORDER BY nombre')
            deportes = cur.fetchall()

    return render_template('admin/campeonatos.html', titulo='Admin · Campeonatos', campeonatos=campeonatos, deportes=deportes)


@admin_bp.route('/campeonatos', methods=['POST'])
def campeonatos_crear():
    nombre = request.form.get('nombre')
    deporte_id = request.form.get('deporte_id')
    fecha_inicio = request.form.get('fecha_inicio') or None
    fecha_fin = request.form.get('fecha_fin') or None
    descripcion = request.form.get('descripcion') or None

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """INSERT INTO campeonatos (nombre, deporte_id, fecha_inicio, fecha_fin, descripcion)
                   VALUES (%s, %s, %s, %s, %s)""",
                (nombre, deporte_id, fecha_inicio, fecha_fin, descripcion),
            )
    return redirect('/admin/campeonatos')


@admin_bp.route('/campeonatos/<int:id>/editar')
def campeonatos_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM campeonatos WHERE id = %s', (id,))
            campeonato = cur.fetchone()
            if not campeonato:
                abort(404)
            cur.execute('SELECT * FROM deportes ORDER BY nombre')
            deportes = cur.fetchall()

    return render_template('admin/campeonatos_editar.html', titulo='Admin · Editar campeonato', campeonato=campeonato, deportes=deportes)


@admin_bp.route('/campeonatos/<int:id>/editar', methods=['POST'])
def campeonatos_editar(id):
    nombre = request.form.get('nombre')
    deporte_id = request.form.get('deporte_id')
    fecha_inicio = request.form.get('fecha_inicio') or None
    fecha_fin = request.form.get('fecha_fin') or None
    descripcion = request.form.get('descripcion') or None

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """UPDATE campeonatos SET nombre = %s, deporte_id = %s, fecha_inicio = %s, fecha_fin = %s, descripcion = %s
                   WHERE id = %s""",
                (nombre, deporte_id, fecha_inicio, fecha_fin, descripcion, id),
            )
    return redirect('/admin/campeonatos')


@admin_bp.route('/campeonatos/<int:id>/eliminar', methods=['POST'])
def campeonatos_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM campeonatos WHERE id = %s', (id,))
    return redirect('/admin/campeonatos')
