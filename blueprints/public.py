from flask import Blueprint, render_template, request, abort
from db import obtener_conexion

public_bp = Blueprint('public', __name__)


def _agrupar_por_nivel(filas):
    grupos = {'punta': [], 'medio': [], 'base': []}
    for r in filas:
        nivel = r['nivel'] if r['nivel'] in ('punta', 'medio', 'base') else 'base'
        grupos[nivel].append(r)
    return grupos


def _recortar_para_inicio(grupos):
    """Vista previa para el inicio: si hay punta, la punta completa + hasta 3 mas;
    si no hay punta, solo las primeras 3."""
    resto = grupos['medio'] + grupos['base']
    if len(grupos['punta']) > 0:
        return {'punta': grupos['punta'], 'medio': resto[:3], 'base': []}
    return {'punta': [], 'medio': resto[:3], 'base': []}


@public_bp.route('/')
def home():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM eventos ORDER BY fecha DESC LIMIT 6')
            eventos = cur.fetchall()

            cur.execute('SELECT * FROM noticias ORDER BY fecha DESC LIMIT 3')
            noticias = cur.fetchall()

            cur.execute("""
                SELECT * FROM icfes_resultados
                WHERE anio = (SELECT MAX(anio) FROM icfes_resultados)
                ORDER BY puntaje DESC, creado_en ASC
                LIMIT 3
            """)
            icfes_resultados = cur.fetchall()

            cur.execute('SELECT * FROM gobierno_escolar ORDER BY orden, nombre')
            gobierno_escolar = cur.fetchall()

            cur.execute('SELECT * FROM equipo_desarrollo ORDER BY orden, nombre')
            equipo_desarrollo = cur.fetchall()

            cur.execute('SELECT * FROM comite_ecologico ORDER BY orden, nombre')
            comite_ecologico = cur.fetchall()

            cur.execute('SELECT * FROM equipo_drones ORDER BY orden, nombre')
            equipo_drones = cur.fetchall()

            cur.execute('SELECT * FROM coheteria ORDER BY orden, nombre')
            coheteria = cur.fetchall()

            cur.execute('SELECT himno_url, fondo_url FROM institucion_info ORDER BY id LIMIT 1')
            info = cur.fetchone()

            cur.execute("SELECT url FROM galeria_fotos WHERE seccion = 'inicio' AND visible = true ORDER BY orden, id")
            hero_fotos = cur.fetchall()

    return render_template(
        'home.html',
        titulo='Inicio',
        eventos=eventos,
        noticias=noticias,
        icfesResultados=icfes_resultados,
        icfesAnio=icfes_resultados[0]['anio'] if icfes_resultados else None,
        gobiernoEscolar=_recortar_para_inicio(_agrupar_por_nivel(gobierno_escolar)),
        equipoDesarrollo=_recortar_para_inicio(_agrupar_por_nivel(equipo_desarrollo)),
        comiteEcologico=_recortar_para_inicio(_agrupar_por_nivel(comite_ecologico)),
        equipoDrones=_recortar_para_inicio(_agrupar_por_nivel(equipo_drones)),
        coheteria=_recortar_para_inicio(_agrupar_por_nivel(coheteria)),
        himnoUrl=info['himno_url'] if info else None,
        fondoUrl=info['fondo_url'] if info else None,
        heroImagenes=[f['url'] for f in hero_fotos],
    )


@public_bp.route('/gobierno-escolar')
def gobierno_escolar():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM gobierno_escolar ORDER BY orden, nombre')
            miembros = cur.fetchall()
    return render_template('gobierno_escolar.html', titulo='Gobierno Escolar', grupos=_agrupar_por_nivel(miembros))


@public_bp.route('/equipo-desarrollo')
def equipo_desarrollo():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM equipo_desarrollo ORDER BY orden, nombre')
            miembros = cur.fetchall()
            cur.execute('SELECT equipo_desarrollo_texto, equipo_desarrollo_portada_url FROM institucion_info ORDER BY id LIMIT 1')
            info = cur.fetchone()
            cur.execute("SELECT * FROM galeria_fotos WHERE seccion = 'equipo-desarrollo' AND visible = true ORDER BY orden, creado_en")
            fotos = cur.fetchall()
    return render_template(
        'equipo_desarrollo.html',
        titulo='Equipo de Desarrollo',
        grupos=_agrupar_por_nivel(miembros),
        texto=info['equipo_desarrollo_texto'] if info else None,
        portada=info['equipo_desarrollo_portada_url'] if info else None,
        fotos=fotos,
    )


@public_bp.route('/comite-ecologico')
def comite_ecologico():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM comite_ecologico ORDER BY orden, nombre')
            miembros = cur.fetchall()
            cur.execute('SELECT comite_ecologico_texto, comite_ecologico_portada_url FROM institucion_info ORDER BY id LIMIT 1')
            info = cur.fetchone()
            cur.execute("SELECT * FROM galeria_fotos WHERE seccion = 'comite-ecologico' AND visible = true ORDER BY orden, creado_en")
            fotos = cur.fetchall()
    return render_template(
        'comite_ecologico.html',
        titulo='Comité Ecológico',
        grupos=_agrupar_por_nivel(miembros),
        texto=info['comite_ecologico_texto'] if info else None,
        portada=info['comite_ecologico_portada_url'] if info else None,
        fotos=fotos,
    )


@public_bp.route('/equipo-drones')
def equipo_drones():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM equipo_drones ORDER BY orden, nombre')
            miembros = cur.fetchall()
            cur.execute('SELECT equipo_drones_texto, equipo_drones_portada_url FROM institucion_info ORDER BY id LIMIT 1')
            info = cur.fetchone()
            cur.execute("SELECT * FROM galeria_fotos WHERE seccion = 'equipo-drones' AND visible = true ORDER BY orden, creado_en")
            fotos = cur.fetchall()
    return render_template(
        'equipo_drones.html',
        titulo='Equipo de Drones',
        grupos=_agrupar_por_nivel(miembros),
        texto=info['equipo_drones_texto'] if info else None,
        portada=info['equipo_drones_portada_url'] if info else None,
        fotos=fotos,
    )


@public_bp.route('/coheteria')
def coheteria():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM coheteria ORDER BY orden, nombre')
            miembros = cur.fetchall()
            cur.execute('SELECT coheteria_texto, coheteria_portada_url FROM institucion_info ORDER BY id LIMIT 1')
            info = cur.fetchone()
            cur.execute("SELECT * FROM galeria_fotos WHERE seccion = 'coheteria' AND visible = true ORDER BY orden, creado_en")
            fotos = cur.fetchall()
    return render_template(
        'coheteria.html',
        titulo='Cohetería',
        grupos=_agrupar_por_nivel(miembros),
        texto=info['coheteria_texto'] if info else None,
        portada=info['coheteria_portada_url'] if info else None,
        fotos=fotos,
    )


@public_bp.route('/institucion')
def institucion():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM institucion_info ORDER BY id LIMIT 1')
            info = cur.fetchone()
    return render_template('institucion.html', titulo='Institución', info=info)


@public_bp.route('/articulado')
def articulado():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT articulado_texto FROM institucion_info ORDER BY id LIMIT 1')
            info = cur.fetchone()
            cur.execute('SELECT * FROM media_tecnica_categorias ORDER BY orden, nombre')
            categorias = cur.fetchall()
    return render_template(
        'articulado.html',
        titulo='Articulado',
        texto=info['articulado_texto'] if info else None,
        categorias=categorias,
    )


@public_bp.route('/articulado/<int:id>')
def media_tecnica_detalle(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM media_tecnica_categorias WHERE id = %s', (id,))
            categoria = cur.fetchone()
            if not categoria:
                abort(404)
            cur.execute(
                'SELECT * FROM galeria_fotos WHERE media_tecnica_categoria_id = %s AND visible = true ORDER BY orden, creado_en',
                (id,)
            )
            fotos = cur.fetchall()
    return render_template('media_tecnica_detalle.html', titulo=categoria['nombre'], categoria=categoria, fotos=fotos)


@public_bp.route('/investigacion')
def investigacion():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT investigacion_texto FROM institucion_info ORDER BY id LIMIT 1')
            info = cur.fetchone()
    return render_template('investigacion.html', titulo='Investigación', texto=info['investigacion_texto'] if info else None)


@public_bp.route('/comunidad-educativa')
def comunidad_educativa():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("SELECT * FROM comunidad_educativa WHERE categoria IN ('rectoria', 'coordinacion') ORDER BY orden, nombre")
            directivos = cur.fetchall()
            cur.execute("SELECT * FROM comunidad_educativa WHERE categoria = 'docente' ORDER BY orden, nombre LIMIT 4")
            docentes_preview = cur.fetchall()
            cur.execute("SELECT COUNT(*) AS total FROM comunidad_educativa WHERE categoria = 'docente'")
            total_docentes = cur.fetchone()['total']

    return render_template(
        'comunidad_educativa.html',
        titulo='Comunidad Educativa',
        directivos=_agrupar_por_nivel(directivos),
        docentesPreview=docentes_preview,
        totalDocentes=total_docentes,
    )


@public_bp.route('/comunidad-educativa/docentes')
def docentes():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("SELECT * FROM comunidad_educativa WHERE categoria = 'docente' ORDER BY orden, nombre")
            lista_docentes = cur.fetchall()

    areas = list(dict.fromkeys(d['area'] for d in lista_docentes if d['area']))
    materias = set(d['materia'] for d in lista_docentes if d['materia'])
    anios_combinados = sum(d['anios_experiencia'] or 0 for d in lista_docentes)

    return render_template(
        'comunidad_docentes.html',
        titulo='Nuestro Cuerpo de Docentes',
        docentes=lista_docentes,
        areas=areas,
        totalAsignaturas=len(materias),
        aniosCombinados=anios_combinados,
    )


@public_bp.route('/himno')
def himno():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT himno_url, himno_letra FROM institucion_info ORDER BY id LIMIT 1')
            info = cur.fetchone()

    return render_template(
        'himno.html',
        titulo='Himno Escolar',
        himnoUrl=info['himno_url'] if info else None,
        himnoLetra=info['himno_letra'] if info else None,
    )


@public_bp.route('/noticias')
def noticias():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM noticias ORDER BY fecha DESC')
            lista = cur.fetchall()
    return render_template('noticias.html', titulo='Noticias', noticias=lista)


@public_bp.route('/noticias/<int:id>')
def noticia_detalle(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM noticias WHERE id = %s', (id,))
            noticia = cur.fetchone()
            if not noticia:
                abort(404)
            cur.execute('SELECT * FROM galeria_fotos WHERE noticia_id = %s AND visible = true ORDER BY orden, creado_en', (id,))
            fotos = cur.fetchall()

    return render_template('noticia_detalle.html', titulo=noticia['titulo'], noticia=noticia, fotos=fotos)


@public_bp.route('/eventos')
def eventos():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM eventos ORDER BY fecha DESC')
            lista = cur.fetchall()
    return render_template('eventos.html', titulo='Eventos', eventos=lista)


@public_bp.route('/eventos/<int:id>')
def evento_detalle(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM eventos WHERE id = %s', (id,))
            evento = cur.fetchone()
            if not evento:
                abort(404)
            cur.execute('SELECT * FROM galeria_fotos WHERE evento_id = %s AND visible = true ORDER BY orden, creado_en', (id,))
            fotos = cur.fetchall()

    return render_template('evento_detalle.html', titulo=evento['titulo'], evento=evento, fotos=fotos)


@public_bp.route('/grupos-estudiantiles')
def grupos_estudiantiles():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM grupos_estudiantiles ORDER BY nombre')
            grupos = cur.fetchall()
    return render_template('grupos_estudiantiles.html', titulo='Grupos y Semilleros', grupos=grupos)


@public_bp.route('/deportes')
def deportes():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM deportes ORDER BY nombre')
            lista_deportes = cur.fetchall()
            cur.execute("""
                SELECT equipos.*, deportes.nombre AS deporte_nombre
                FROM equipos
                JOIN deportes ON deportes.id = equipos.deporte_id
                ORDER BY deportes.nombre, equipos.nombre
            """)
            equipos = cur.fetchall()
    return render_template('deportes.html', titulo='Equipos deportivos', deportes=lista_deportes, equipos=equipos)


@public_bp.route('/deportes/<int:id>')
def deporte_detalle(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM deportes WHERE id = %s', (id,))
            deporte = cur.fetchone()
            if not deporte:
                abort(404)
            cur.execute('SELECT * FROM equipos WHERE deporte_id = %s ORDER BY nombre', (id,))
            equipos = cur.fetchall()
    return render_template('deporte_detalle.html', titulo=deporte['nombre'], deporte=deporte, equipos=equipos)


@public_bp.route('/campeonatos')
def campeonatos():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("""
                SELECT campeonatos.*, deportes.nombre AS deporte_nombre
                FROM campeonatos
                JOIN deportes ON deportes.id = campeonatos.deporte_id
                ORDER BY campeonatos.fecha_inicio DESC
            """)
            lista = cur.fetchall()
    return render_template('campeonatos.html', titulo='Intercursos', campeonatos=lista)


@public_bp.route('/campeonatos/<int:id>')
def campeonato_detalle(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("""
                SELECT campeonatos.*, deportes.nombre AS deporte_nombre
                FROM campeonatos
                JOIN deportes ON deportes.id = campeonatos.deporte_id
                WHERE campeonatos.id = %s
            """, (id,))
            campeonato = cur.fetchone()
            if not campeonato:
                abort(404)

            cur.execute("""
                SELECT resultados.*, el.nombre AS equipo_local_nombre, ev.nombre AS equipo_visitante_nombre
                FROM resultados
                JOIN equipos el ON el.id = resultados.equipo_local_id
                JOIN equipos ev ON ev.id = resultados.equipo_visitante_id
                WHERE resultados.campeonato_id = %s
                ORDER BY resultados.fecha
            """, (id,))
            resultados = cur.fetchall()

    return render_template(
        'campeonato_detalle.html', titulo=campeonato['nombre'], campeonato=campeonato, resultados=resultados,
    )


@public_bp.route('/mejores-puestos')
def mejores_puestos():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("""
                SELECT mejores_puestos.*, estudiantes.nombres, estudiantes.apellidos, grados.nombre AS grado_nombre
                FROM mejores_puestos
                JOIN estudiantes ON estudiantes.id = mejores_puestos.estudiante_id
                JOIN grados ON grados.id = mejores_puestos.grado_id
                ORDER BY grados.nivel, mejores_puestos.periodo DESC, mejores_puestos.puesto
            """)
            puestos = cur.fetchall()
    return render_template('mejores_puestos.html', titulo='Puestos de honor', puestos=puestos)


def _agrupar_por_anio(filas):
    grupos = []
    grupo_actual = None

    for r in filas:
        if grupo_actual is None or grupo_actual['anio'] != r['anio']:
            grupo_actual = {'anio': r['anio'], 'resultados': []}
            grupos.append(grupo_actual)
        grupo_actual['resultados'].append(r)

    return grupos


@public_bp.route('/icfes')
def icfes():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM icfes_resultados ORDER BY anio DESC, puntaje DESC')
            resultados = cur.fetchall()
    return render_template('icfes.html', titulo='Mejores ICFES', grupos=_agrupar_por_anio(resultados))


@public_bp.route('/alianzas')
def alianzas():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM alianzas ORDER BY nombre')
            lista = cur.fetchall()
    return render_template('alianzas.html', titulo='Alianzas', alianzas=lista)


MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
         'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']


def _agrupar_por_mes(filas):
    grupos = []
    grupo_actual = None

    for foto in filas:
        fecha = foto['fecha']
        clave = (fecha.year, fecha.month)

        if grupo_actual is None or grupo_actual['clave'] != clave:
            mes = MESES[fecha.month - 1]
            grupo_actual = {
                'clave': clave,
                'etiqueta': f'{mes.capitalize()} {fecha.year}',
                'fotos': [],
            }
            grupos.append(grupo_actual)
        grupo_actual['fotos'].append(foto)

    return grupos


@public_bp.route('/galeria')
def galeria():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                "SELECT * FROM galeria_fotos WHERE visible = true AND (seccion IS NULL OR seccion <> 'inicio') ORDER BY fecha DESC, creado_en DESC"
            )
            fotos = cur.fetchall()
    return render_template('galeria.html', titulo='Galeria', grupos=_agrupar_por_mes(fotos))


@public_bp.route('/contacto', methods=['GET'])
def contacto_form():
    return render_template('contacto.html', titulo='Contacto', enviado=False, error=None)


@public_bp.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')

    if not nombre or not email or not mensaje:
        return render_template(
            'contacto.html', titulo='Contacto', enviado=False, error='Todos los campos son obligatorios',
        ), 400

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'INSERT INTO mensajes_contacto (nombre, apellido, email, mensaje) VALUES (%s, %s, %s, %s)',
                (nombre, apellido or None, email, mensaje),
            )

    return render_template('contacto.html', titulo='Contacto', enviado=True, error=None)
