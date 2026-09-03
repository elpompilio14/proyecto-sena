from datetime import date
from flask import render_template, request, redirect, abort, jsonify
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo, TIPOS_IMAGEN_Y_VIDEO

SECCIONES = {
    'coheteria': 'Cohetería',
    'comite-ecologico': 'Comité Ecológico',
    'equipo-drones': 'Equipo de Drones',
    'equipo-desarrollo': 'Equipo de Desarrollo',
}


@admin_bp.route('/fotos')
def fotos_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("""
                SELECT galeria_fotos.*, eventos.titulo AS evento_titulo, noticias.titulo AS noticia_titulo,
                    media_tecnica_categorias.nombre AS media_tecnica_nombre
                FROM galeria_fotos
                LEFT JOIN eventos ON eventos.id = galeria_fotos.evento_id
                LEFT JOIN noticias ON noticias.id = galeria_fotos.noticia_id
                LEFT JOIN media_tecnica_categorias ON media_tecnica_categorias.id = galeria_fotos.media_tecnica_categoria_id
                ORDER BY galeria_fotos.fecha DESC, galeria_fotos.creado_en DESC
            """)
            fotos = cur.fetchall()
            cur.execute('SELECT id, titulo FROM eventos ORDER BY fecha DESC')
            eventos = cur.fetchall()
            cur.execute('SELECT id, titulo FROM noticias ORDER BY fecha DESC')
            noticias = cur.fetchall()
            cur.execute('SELECT id, nombre FROM media_tecnica_categorias ORDER BY orden, nombre')
            categorias_media_tecnica = cur.fetchall()

    fotos_con_seccion = []
    for f in fotos:
        fila = dict(f)
        fila['seccion_nombre'] = SECCIONES.get(f['seccion'])
        fotos_con_seccion.append(fila)

    return render_template(
        'admin/fotos.html',
        titulo='Admin · Galería',
        fotos=fotos_con_seccion,
        eventos=eventos,
        noticias=noticias,
        categoriasMediaTecnica=categorias_media_tecnica,
        secciones=SECCIONES,
    )


@admin_bp.route('/fotos', methods=['POST'])
def fotos_crear():
    archivos = request.files.getlist('imagenes')
    archivos = [a for a in archivos if a and a.filename]
    if not archivos:
        return redirect('/admin/fotos')

    titulo = request.form.get('titulo')
    evento_id = request.form.get('evento_id') or None
    noticia_id = request.form.get('noticia_id') or None
    media_tecnica_categoria_id = request.form.get('media_tecnica_categoria_id') or None
    seccion = request.form.get('seccion') or None
    fecha = request.form.get('fecha') or date.today().isoformat()
    orden = request.form.get('orden') or 1

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            for archivo in archivos:
                url = guardar_archivo(archivo, TIPOS_IMAGEN_Y_VIDEO)
                cur.execute(
                    """INSERT INTO galeria_fotos (titulo, url, evento_id, noticia_id, media_tecnica_categoria_id, seccion, fecha, orden)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (titulo or None, url, evento_id, noticia_id, media_tecnica_categoria_id, seccion, fecha, orden),
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
            cur.execute('SELECT id, nombre FROM media_tecnica_categorias ORDER BY orden, nombre')
            categorias_media_tecnica = cur.fetchall()

    return render_template(
        'admin/fotos_editar.html',
        titulo='Admin · Editar foto',
        foto=foto,
        eventos=eventos,
        noticias=noticias,
        categoriasMediaTecnica=categorias_media_tecnica,
        secciones=SECCIONES,
    )


@admin_bp.route('/fotos/<int:id>/editar', methods=['POST'])
def fotos_editar(id):
    titulo = request.form.get('titulo')
    evento_id = request.form.get('evento_id') or None
    noticia_id = request.form.get('noticia_id') or None
    media_tecnica_categoria_id = request.form.get('media_tecnica_categoria_id') or None
    seccion = request.form.get('seccion') or None
    url_actual = request.form.get('url_actual')
    url = guardar_archivo(request.files.get('imagen'), TIPOS_IMAGEN_Y_VIDEO) or url_actual
    fecha = request.form.get('fecha') or date.today().isoformat()
    orden = request.form.get('orden') or 1

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """UPDATE galeria_fotos SET titulo = %s, url = %s, evento_id = %s, noticia_id = %s,
                       media_tecnica_categoria_id = %s, seccion = %s, fecha = %s, orden = %s
                   WHERE id = %s""",
                (titulo or None, url, evento_id, noticia_id, media_tecnica_categoria_id, seccion, fecha, orden, id),
            )
    return redirect('/admin/fotos')


@admin_bp.route('/fotos/<int:id>/eliminar', methods=['POST'])
def fotos_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM galeria_fotos WHERE id = %s', (id,))
    return redirect('/admin/fotos')


@admin_bp.route('/fotos/<int:id>/visibilidad', methods=['POST'])
def fotos_toggle_visible(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('UPDATE galeria_fotos SET visible = NOT visible WHERE id = %s RETURNING visible', (id,))
            resultado = cur.fetchone()
    return jsonify({'visible': resultado['visible']})


@admin_bp.route('/fotos/editar-lote', methods=['POST'])
def fotos_editar_lote():
    ids = request.form.getlist('ids')
    if not ids:
        return redirect('/admin/fotos')

    evento_lote = request.form.get('evento_lote')
    media_tecnica_categoria_lote = request.form.get('media_tecnica_categoria_lote')
    seccion_lote = request.form.get('seccion_lote')
    fecha_lote = request.form.get('fecha_lote')
    titulo_lote = request.form.get('titulo_lote')
    orden_lote = request.form.get('orden_lote')

    cambios = []
    valores = []

    if evento_lote is not None and evento_lote != '__no_cambiar__':
        cambios.append('evento_id = %s')
        valores.append(evento_lote or None)
    if media_tecnica_categoria_lote is not None and media_tecnica_categoria_lote != '__no_cambiar__':
        cambios.append('media_tecnica_categoria_id = %s')
        valores.append(media_tecnica_categoria_lote or None)
    if seccion_lote is not None and seccion_lote != '__no_cambiar__':
        cambios.append('seccion = %s')
        valores.append(seccion_lote or None)
    if fecha_lote:
        cambios.append('fecha = %s')
        valores.append(fecha_lote)
    if titulo_lote:
        cambios.append('titulo = %s')
        valores.append(titulo_lote)
    if orden_lote:
        cambios.append('orden = %s')
        valores.append(orden_lote)

    if cambios:
        valores.append(ids)
        with obtener_conexion() as conexion:
            with conexion.cursor() as cur:
                cur.execute(
                    f"UPDATE galeria_fotos SET {', '.join(cambios)} WHERE id = ANY(%s::int[])",
                    valores,
                )

    return redirect('/admin/fotos')
