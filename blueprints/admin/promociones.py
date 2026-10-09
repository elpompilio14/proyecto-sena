from datetime import date
from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo, TIPOS_IMAGEN_Y_VIDEO


def _datos_formulario(f):
    """Campos de una promocion tal como vienen del formulario (los archivos se suben aqui)."""
    logo_url = guardar_archivo(request.files.get('logo')) or (f.get('logo_actual') or None)
    portada_url = guardar_archivo(request.files.get('portada')) or (f.get('portada_actual') or None)
    return (
        f.get('nombre') or None, f.get('anio') or None, f.get('lema') or None,
        f.get('descripcion') or None, logo_url, portada_url,
    )


@admin_bp.route('/promociones')
def promociones_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """SELECT p.*, (SELECT count(*) FROM galeria_fotos g WHERE g.promocion_id = p.id) AS num_fotos
                   FROM promociones p ORDER BY p.anio DESC NULLS LAST, p.id DESC"""
            )
            promociones = cur.fetchall()
    actual = next((p for p in promociones if p['actual']), None)
    pasadas = [p for p in promociones if not p['actual']]
    return render_template('admin/promociones.html', titulo='Admin · Promociones', actual=actual, pasadas=pasadas)


@admin_bp.route('/promociones', methods=['POST'])
def promociones_crear():
    es_actual = request.form.get('es_actual') == '1'
    datos = _datos_formulario(request.form)
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            if es_actual:
                cur.execute('UPDATE promociones SET actual = false WHERE actual')
            cur.execute(
                """INSERT INTO promociones (nombre, anio, lema, descripcion, logo_url, portada_url, actual)
                   VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                datos + (es_actual,),
            )
            nueva = cur.fetchone()
    return redirect(f"/admin/promociones/{nueva['id']}")


@admin_bp.route('/promociones/<int:id>')
def promociones_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM promociones WHERE id = %s', (id,))
            promocion = cur.fetchone()
            if not promocion:
                abort(404)
            cur.execute('SELECT * FROM galeria_fotos WHERE promocion_id = %s ORDER BY orden, creado_en', (id,))
            fotos = cur.fetchall()
    return render_template('admin/promociones_editar.html', titulo='Admin · Editar promoción', promocion=promocion, fotos=fotos)


@admin_bp.route('/promociones/<int:id>', methods=['POST'])
def promociones_editar(id):
    datos = _datos_formulario(request.form)
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """UPDATE promociones SET nombre = %s, anio = %s, lema = %s, descripcion = %s,
                       logo_url = %s, portada_url = %s
                   WHERE id = %s""",
                datos + (id,),
            )
    return redirect(f'/admin/promociones/{id}')


@admin_bp.route('/promociones/<int:id>/archivar', methods=['POST'])
def promociones_archivar(id):
    """Pasa la promocion actual (con todas sus fotos) a promociones pasadas."""
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('UPDATE promociones SET actual = false WHERE id = %s', (id,))
    return redirect('/admin/promociones')


@admin_bp.route('/promociones/<int:id>/eliminar', methods=['POST'])
def promociones_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM promociones WHERE id = %s', (id,))
    return redirect('/admin/promociones')


@admin_bp.route('/promociones/<int:id>/fotos', methods=['POST'])
def promociones_subir_fotos(id):
    archivos = [a for a in request.files.getlist('fotos') if a and a.filename]
    titulo = request.form.get('titulo') or None
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            for archivo in archivos:
                url = guardar_archivo(archivo, TIPOS_IMAGEN_Y_VIDEO)
                cur.execute(
                    'INSERT INTO galeria_fotos (titulo, url, promocion_id, fecha, orden) VALUES (%s, %s, %s, %s, 1)',
                    (titulo, url, id, date.today().isoformat()),
                )
    return redirect(f'/admin/promociones/{id}')


@admin_bp.route('/promociones/<int:id>/fotos/<int:foto_id>/eliminar', methods=['POST'])
def promociones_eliminar_foto(id, foto_id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM galeria_fotos WHERE id = %s AND promocion_id = %s', (foto_id, id))
    return redirect(f'/admin/promociones/{id}')
