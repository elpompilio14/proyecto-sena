from datetime import date
from flask import render_template, request, redirect
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo, TIPOS_IMAGEN_Y_VIDEO


@admin_bp.route('/promocion')
def promocion_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """SELECT promocion_nombre, promocion_anio, promocion_lema, promocion_descripcion,
                          promocion_logo_url, promocion_portada_url
                   FROM institucion_info ORDER BY id LIMIT 1"""
            )
            info = cur.fetchone() or {}
            cur.execute("SELECT * FROM galeria_fotos WHERE seccion = 'promocion' ORDER BY orden, creado_en")
            fotos = cur.fetchall()
    return render_template('admin/promocion.html', titulo='Admin · Promoción actual', info=info, fotos=fotos)


@admin_bp.route('/promocion/info', methods=['POST'])
def promocion_actualizar_info():
    f = request.form
    logo_url = guardar_archivo(request.files.get('logo')) or (f.get('logo_actual') or None)
    portada_url = guardar_archivo(request.files.get('portada')) or (f.get('portada_actual') or None)
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """UPDATE institucion_info
                   SET promocion_nombre = %s, promocion_anio = %s, promocion_lema = %s,
                       promocion_descripcion = %s, promocion_logo_url = %s, promocion_portada_url = %s
                   WHERE id = (SELECT id FROM institucion_info ORDER BY id LIMIT 1)""",
                (
                    f.get('nombre') or None, f.get('anio') or None, f.get('lema') or None,
                    f.get('descripcion') or None, logo_url, portada_url,
                ),
            )
    return redirect('/admin/promocion')


@admin_bp.route('/promocion/fotos', methods=['POST'])
def promocion_subir_fotos():
    archivos = [a for a in request.files.getlist('fotos') if a and a.filename]
    titulo = request.form.get('titulo') or None
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            for archivo in archivos:
                url = guardar_archivo(archivo, TIPOS_IMAGEN_Y_VIDEO)
                cur.execute(
                    "INSERT INTO galeria_fotos (titulo, url, seccion, fecha, orden) VALUES (%s, %s, 'promocion', %s, 1)",
                    (titulo, url, date.today().isoformat()),
                )
    return redirect('/admin/promocion')


@admin_bp.route('/promocion/fotos/<int:id>/eliminar', methods=['POST'])
def promocion_eliminar_foto(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("DELETE FROM galeria_fotos WHERE id = %s AND seccion = 'promocion'", (id,))
    return redirect('/admin/promocion')
