from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


@admin_bp.route('/grupos-estudiantiles')
def grupos_estudiantiles_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM grupos_estudiantiles ORDER BY nombre')
            grupos = cur.fetchall()
    return render_template('admin/grupos_estudiantiles.html', titulo='Admin · Grupos Estudiantiles', grupos=grupos)


@admin_bp.route('/grupos-estudiantiles', methods=['POST'])
def grupos_estudiantiles_crear():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion') or None
    encargado = request.form.get('encargado') or None
    foto_url = guardar_archivo(request.files.get('imagen'))

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'INSERT INTO grupos_estudiantiles (nombre, descripcion, encargado, foto_url) VALUES (%s, %s, %s, %s)',
                (nombre, descripcion, encargado, foto_url),
            )
    return redirect('/admin/grupos-estudiantiles')


@admin_bp.route('/grupos-estudiantiles/<int:id>/editar')
def grupos_estudiantiles_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM grupos_estudiantiles WHERE id = %s', (id,))
            grupo = cur.fetchone()
    if not grupo:
        abort(404)
    return render_template('admin/grupos_estudiantiles_editar.html', titulo='Admin · Editar grupo', grupo=grupo)


@admin_bp.route('/grupos-estudiantiles/<int:id>/editar', methods=['POST'])
def grupos_estudiantiles_editar(id):
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion') or None
    encargado = request.form.get('encargado') or None
    foto_actual = request.form.get('foto_actual')
    foto_url = guardar_archivo(request.files.get('imagen')) or (foto_actual or None)

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE grupos_estudiantiles SET nombre = %s, descripcion = %s, encargado = %s, foto_url = %s WHERE id = %s',
                (nombre, descripcion, encargado, foto_url, id),
            )
    return redirect('/admin/grupos-estudiantiles')


@admin_bp.route('/grupos-estudiantiles/<int:id>/eliminar', methods=['POST'])
def grupos_estudiantiles_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM grupos_estudiantiles WHERE id = %s', (id,))
    return redirect('/admin/grupos-estudiantiles')
