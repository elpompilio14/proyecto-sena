from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/comite-ecologico')
def comite_ecologico_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM comite_ecologico ORDER BY orden, nombre')
            miembros = cur.fetchall()
    return render_template('admin/comite_ecologico.html', titulo='Admin · Comité Ecológico', miembros=miembros)


@admin_bp.route('/comite-ecologico', methods=['POST'])
def comite_ecologico_crear():
    nombre = request.form.get('nombre')
    rol = request.form.get('rol') or None
    foto_url = guardar_archivo(request.files.get('imagen'))
    orden = request.form.get('orden') or 0

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'INSERT INTO comite_ecologico (nombre, rol, foto_url, orden) VALUES (%s, %s, %s, %s)',
                (nombre, rol, foto_url, orden),
            )
    return redirect('/admin/comite-ecologico')


@admin_bp.route('/comite-ecologico/<int:id>/editar')
def comite_ecologico_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM comite_ecologico WHERE id = %s', (id,))
            miembro = cur.fetchone()
    if not miembro:
        abort(404)
    return render_template('admin/comite_ecologico_editar.html', titulo='Admin · Editar miembro', miembro=miembro)


@admin_bp.route('/comite-ecologico/<int:id>/editar', methods=['POST'])
def comite_ecologico_editar(id):
    nombre = request.form.get('nombre')
    rol = request.form.get('rol') or None
    foto_actual = request.form.get('foto_actual')
    foto_url = guardar_archivo(request.files.get('imagen')) or (foto_actual or None)
    orden = request.form.get('orden') or 0

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE comite_ecologico SET nombre = %s, rol = %s, foto_url = %s, orden = %s WHERE id = %s',
                (nombre, rol, foto_url, orden, id),
            )
    return redirect('/admin/comite-ecologico')


@admin_bp.route('/comite-ecologico/<int:id>/eliminar', methods=['POST'])
def comite_ecologico_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM comite_ecologico WHERE id = %s', (id,))
    return redirect('/admin/comite-ecologico')
