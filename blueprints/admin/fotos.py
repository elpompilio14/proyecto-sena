from datetime import date
from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo, TIPOS_IMAGEN_Y_VIDEO


@admin_bp.route('/fotos')
def fotos_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("""
                SELECT galeria_fotos.*, eventos.titulo AS evento_titulo, noticias.titulo AS noticia_titulo
                FROM galeria_fotos
                LEFT JOIN eventos ON eventos.id = galeria_fotos.evento_id
                LEFT JOIN noticias ON noticias.id = galeria_fotos.noticia_id
                ORDER BY galeria_fotos.fecha DESC, galeria_fotos.creado_en DESC
            """)
            fotos = cur.fetchall()
            cur.execute('SELECT id, titulo FROM eventos ORDER BY fecha DESC')
            eventos = cur.fetchall()
            cur.execute('SELECT id, titulo FROM noticias ORDER BY fecha DESC')
            noticias = cur.fetchall()

    return render_template('admin/fotos.html', titulo='Admin · Galería', fotos=fotos, eventos=eventos, noticias=noticias)


@admin_bp.route('/fotos', methods=['POST'])
def fotos_crear():
    archivos = request.files.getlist('imagenes')
    archivos = [a for a in archivos if a and a.filename]
    if not archivos:
        return redirect('/admin/fotos')

    titulo = request.form.get('titulo')
    evento_id = request.form.get('evento_id') or None
    noticia_id = request.form.get('noticia_id') or None
    fecha = request.form.get('fecha') or date.today().isoformat()

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            for archivo in archivos:
                url = guardar_archivo(archivo, TIPOS_IMAGEN_Y_VIDEO)
                cur.execute(
                    'INSERT INTO galeria_fotos (titulo, url, evento_id, noticia_id, fecha) VALUES (%s, %s, %s, %s, %s)',
                    (titulo or None, url, evento_id, noticia_id, fecha),
                )
    return redirect('/admin/fotos')


@admin_bp.route('/fotos/<int:id>/editar')
def fotos_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM galeria_fotos WHERE id = %s', (id,))
            foto = cur.fetchone()
            if not foto:
                abort(404)
            cur.execute('SELECT id, titulo FROM eventos ORDER BY fecha DESC')
            eventos = cur.fetchall()
            cur.execute('SELECT id, titulo FROM noticias ORDER BY fecha DESC')
            noticias = cur.fetchall()

    return render_template('admin/fotos_editar.html', titulo='Admin · Editar foto', foto=foto, eventos=eventos, noticias=noticias)


@admin_bp.route('/fotos/<int:id>/editar', methods=['POST'])
def fotos_editar(id):
    titulo = request.form.get('titulo')
    evento_id = request.form.get('evento_id') or None
    noticia_id = request.form.get('noticia_id') or None
    url_actual = request.form.get('url_actual')
    url = guardar_archivo(request.files.get('imagen'), TIPOS_IMAGEN_Y_VIDEO) or url_actual
    fecha = request.form.get('fecha') or date.today().isoformat()

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'UPDATE galeria_fotos SET titulo = %s, url = %s, evento_id = %s, noticia_id = %s, fecha = %s WHERE id = %s',
                (titulo or None, url, evento_id, noticia_id, fecha, id),
            )
    return redirect('/admin/fotos')


@admin_bp.route('/fotos/<int:id>/eliminar', methods=['POST'])
def fotos_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM galeria_fotos WHERE id = %s', (id,))
    return redirect('/admin/fotos')
