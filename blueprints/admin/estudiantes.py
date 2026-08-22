from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/estudiantes')
def estudiantes_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("""
                SELECT estudiantes.*, grados.nombre AS grado_nombre
                FROM estudiantes
                LEFT JOIN grados ON grados.id = estudiantes.grado_id
                ORDER BY estudiantes.apellidos, estudiantes.nombres
            """)
            estudiantes = cur.fetchall()
            cur.execute('SELECT * FROM grados ORDER BY nivel, nombre')
            grados = cur.fetchall()

    return render_template('admin/estudiantes.html', titulo='Admin · Estudiantes', estudiantes=estudiantes, grados=grados)


@admin_bp.route('/estudiantes', methods=['POST'])
def estudiantes_crear():
    nombres = request.form.get('nombres')
    apellidos = request.form.get('apellidos')
    grado_id = request.form.get('grado_id') or None
    foto_url = guardar_archivo(request.files.get('imagen'))

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'INSERT INTO estudiantes (nombres, apellidos, grado_id, foto_url) VALUES (%s, %s, %s, %s)',
                (nombres, apellidos, grado_id, foto_url),
            )
    return redirect('/admin/estudiantes')


@admin_bp.route('/estudiantes/<int:id>/editar')
def estudiantes_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM estudiantes WHERE id = %s', (id,))
            estudiante = cur.fetchone()
            if not estudiante:
                abort(404)
            cur.execute('SELECT * FROM grados ORDER BY nivel, nombre')
            grados = cur.fetchall()

    return render_template('admin/estudiantes_editar.html', titulo='Admin · Editar estudiante', estudiante=estudiante, grados=grados)


@admin_bp.route('/estudiantes/<int:id>/editar', methods=['POST'])
def estudiantes_editar(id):
    nombres = request.form.get('nombres')
    apellidos = request.form.get('apellidos')
    grado_id = request.form.get('grado_id') or None
    foto_actual = request.form.get('foto_actual')
    foto_url = guardar_archivo(request.files.get('imagen')) or (foto_actual or None)

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE estudiantes SET nombres = %s, apellidos = %s, grado_id = %s, foto_url = %s WHERE id = %s',
                (nombres, apellidos, grado_id, foto_url, id),
            )
    return redirect('/admin/estudiantes')


@admin_bp.route('/estudiantes/<int:id>/eliminar', methods=['POST'])
def estudiantes_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM estudiantes WHERE id = %s', (id,))
    return redirect('/admin/estudiantes')
