from datetime import date
from flask import Blueprint, render_template, request, abort, session
from db import obtener_conexion
from paginas import pagina_oculta_para

public_bp = Blueprint('public', __name__)


@public_bp.before_request
def _bloquear_paginas_ocultas():
    """Las pestanas ocultas desde el admin dan 404 al publico; el admin si puede verlas."""
    usuario = session.get('usuario')
    es_admin = usuario and usuario.get('rol') == 'admin'
    if not es_admin and pagina_oculta_para(request.path):
        abort(404)


def _agrupar_por_nivel(filas):
    grupos = {'punta': [], 'medio': [], 'base': []}
    for r in filas:
        nivel = r['nivel'] if r['nivel'] in ('punta', 'medio', 'base') else 'base'
        grupos[nivel].append(r)
    return grupos


def _con_datos_tarjeta(personas):
    """Agrega a cada persona de la comunidad educativa las filas de su tarjeta que se voltea:
    lo que el admin escribio en 'Datos de la tarjeta' ("Dato: valor" por linea) o, si esta vacio,
    la materia y los anos de experiencia."""
    for p in personas:
        filas = []
        if p.get('tarjeta_datos'):
            for linea in p['tarjeta_datos'].splitlines():
                if not linea.strip():
                    continue
                etiqueta, _, valor = linea.partition(':')
                filas.append([etiqueta.strip(), valor.strip()] if valor else ['', linea.strip()])
        else:
            if p.get('materia'):
                filas.append(['Materia', p['materia']])
            elif p.get('area'):
                filas.append(['Área', p['area']])
            if p.get('anios_experiencia'):
                filas.append(['Experiencia', f"{p['anios_experiencia']} años"])
        p['datos_tarjeta'] = filas
    return personas


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

            cur.execute("SELECT url, titulo FROM galeria_fotos WHERE seccion = 'inicio' AND visible = true ORDER BY orden, id")
            hero_fotos = cur.fetchall()

            # Orla de la comunidad educativa: directivos (rectoria, coordinacion, orientacion) y docentes
            cur.execute(f"""
                SELECT * FROM comunidad_educativa WHERE categoria IN {DIRECTIVOS}
                ORDER BY {ORDEN_DIRECTIVOS}, orden, nombre
            """)
            orla_directivos = _con_datos_tarjeta(cur.fetchall())
            cur.execute("SELECT * FROM comunidad_educativa WHERE categoria = 'docente' ORDER BY orden, nombre")
            orla_docentes = _con_datos_tarjeta(cur.fetchall())

            # Album de deportes (estilo Panini): los jugadores de los grados mas altos primero
            cur.execute('SELECT * FROM deportes ORDER BY nombre')
            lista_deportes = cur.fetchall()
            cur.execute("""
                SELECT deportistas.*, grados.nombre AS grado_nombre, grados.nivel AS grado_nivel
                FROM deportistas
                LEFT JOIN grados ON grados.id = deportistas.grado_id
                ORDER BY grados.nivel DESC NULLS LAST, grados.nombre, deportistas.orden, deportistas.nombre
            """)
            deportistas = cur.fetchall()

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
        heroFotos=hero_fotos,
        albumDeportes=_album_deportes(lista_deportes, deportistas),
        orlaRectoria=[p for p in orla_directivos if p['categoria'] == 'rectoria'],
        orlaDirectivos=[p for p in orla_directivos if p['categoria'] != 'rectoria'],
        orlaDocentes=orla_docentes[:24],
        orlaTotalDocentes=len(orla_docentes),
        anioActual=date.today().year,
    )


def _album_deportes(deportes, deportistas, por_pagina=10):
    """Una 'pagina de album' por deporte con hasta 10 jugadores (los de grados mas altos primero).
    Los deportes sin jugadores no salen."""
    paginas = []
    for d in deportes:
        jugadores = [j for j in deportistas if j['deporte_id'] == d['id']]
        if jugadores:
            paginas.append({
                'deporte': d,
                'sigla': _sigla_deporte(d['nombre']),
                'icono': _icono_deporte(d['nombre']),
                'color': _color_deporte(d['nombre']),
                'jugadores': jugadores[:por_pagina],
                'total': len(jugadores),
            })
    return paginas


def _sigla_deporte(nombre):
    """Codigo corto del deporte para numerar las laminas (como los codigos de pais del album)."""
    nombre = (nombre or '').lower()
    for clave, sigla in (
        ('fut', 'FUT'), ('balonc', 'BSK'), ('basket', 'BSK'), ('balonm', 'BMN'),
        ('vole', 'VOL'), ('badm', 'BDM'), ('bádm', 'BDM'), ('tenis', 'TEN'),
    ):
        if clave in nombre:
            return sigla
    return (nombre[:3] or 'DEP').upper()


def _color_deporte(nombre):
    """Colores de la pagina del album de cada deporte: (principal, acento)."""
    nombre = (nombre or '').lower()
    for clave, colores in (
        ('fut', ('#141414', '#ffffff')),       # negro y blanco
        ('balonc', ('#e8641a', '#141414')),    # naranja y negro
        ('basket', ('#e8641a', '#141414')),
        ('balonm', ('#c8102e', '#ffc61a')),    # rojo y amarillo
        ('vole', ('#0d2b5e', '#ffc61a')),
        ('badm', ('#0d2b5e', '#ffffff')),      # azul oscuro y blanco
        ('bádm', ('#0d2b5e', '#ffffff')),
        ('tenis', ('#2e7d32', '#ffffff')),
    ):
        if clave in nombre:
            return colores
    return ('#0a5ec4', '#ffffff')


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


@public_bp.route('/promociones')
def promociones():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM promociones WHERE actual LIMIT 1')
            actual = cur.fetchone()
            cur.execute('SELECT * FROM promociones WHERE NOT actual ORDER BY anio DESC NULLS LAST, id DESC LIMIT 1')
            ultima_pasada = cur.fetchone()
    return render_template('promociones.html', titulo='Promociones', actual=actual, ultima_pasada=ultima_pasada)


@public_bp.route('/promocion')
def promocion():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM promociones WHERE actual LIMIT 1')
            promocion_actual = cur.fetchone()
            fotos = []
            if promocion_actual:
                cur.execute(
                    'SELECT * FROM galeria_fotos WHERE promocion_id = %s AND visible = true ORDER BY orden, creado_en',
                    (promocion_actual['id'],),
                )
                fotos = cur.fetchall()
    return render_template('promocion.html', titulo='Promoción actual', p=promocion_actual, fotos=fotos)


@public_bp.route('/promociones/pasadas')
def promociones_pasadas():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM promociones WHERE NOT actual ORDER BY anio DESC NULLS LAST, id DESC')
            pasadas = cur.fetchall()
            cur.execute(
                """SELECT g.* FROM galeria_fotos g JOIN promociones p ON p.id = g.promocion_id
                   WHERE NOT p.actual AND g.visible = true ORDER BY g.orden, g.creado_en"""
            )
            fotos_por_promocion = {}
            for f in cur.fetchall():
                fotos_por_promocion.setdefault(f['promocion_id'], []).append(f)
    return render_template(
        'promociones_pasadas.html', titulo='Promociones pasadas',
        pasadas=pasadas, fotos_por_promocion=fotos_por_promocion,
    )


@public_bp.route('/historia')
def historia():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT historia, historia_foto_url, anios_fundacion FROM institucion_info ORDER BY id LIMIT 1')
            intro = cur.fetchone() or {}
            cur.execute('SELECT * FROM historia_bloques WHERE visible = true ORDER BY orden, id')
            bloques = cur.fetchall()
    return render_template('historia.html', titulo='Historia', intro=intro, bloques=bloques)


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
            semilleros = []
            for tabla, nombre, url, icono, resumen in SEMILLEROS:
                cur.execute(f'SELECT COUNT(*) AS total FROM {tabla}')
                semilleros.append({
                    'nombre': nombre, 'url': url, 'icono': icono, 'resumen': resumen,
                    'integrantes': cur.fetchone()['total'],
                })
    return render_template(
        'investigacion.html', titulo='Investigación',
        texto=info['investigacion_texto'] if info else None, semilleros=semilleros,
    )


# Grupos que salen como tarjetas en /investigacion: (tabla, nombre, url, icono, resumen)
SEMILLEROS = [
    ('coheteria', 'Cohetería', '/coheteria', '🚀',
     'Diseñan, construyen y lanzan cohetes poniendo en práctica la física y las matemáticas.'),
    ('equipo_drones', 'Equipo de Drones', '/equipo-drones', '🚁',
     'Aprenden a pilotear, programar y cuidar drones, y los usan en retos y proyectos.'),
    ('equipo_desarrollo', 'Equipo de Desarrollo', '/equipo-desarrollo', '💻',
     'Crean software y herramientas digitales para el colegio, como esta página web.'),
    ('comite_ecologico', 'Comité Ecológico', '/comite-ecologico', '🌱',
     'Promueven el cuidado del medio ambiente con campañas y acciones en la institución.'),
]


@public_bp.route('/comunidad-educativa')
def comunidad_educativa():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(f"SELECT * FROM comunidad_educativa WHERE categoria IN {DIRECTIVOS} ORDER BY orden, nombre")
            directivos = _con_datos_tarjeta(cur.fetchall())
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


# Categorias que salen como directivos (arriba en Comunidad Educativa y en la orla del inicio)
DIRECTIVOS = "('rectoria', 'coordinacion', 'orientacion')"
ORDEN_DIRECTIVOS = "CASE categoria WHEN 'rectoria' THEN 1 WHEN 'coordinacion' THEN 2 ELSE 3 END"


@public_bp.route('/comunidad-educativa/docentes')
def docentes():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("SELECT * FROM comunidad_educativa WHERE categoria = 'docente' ORDER BY orden, nombre")
            lista_docentes = _con_datos_tarjeta(cur.fetchall())

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
            cur.execute('SELECT * FROM grados ORDER BY nivel, nombre')
            grados = cur.fetchall()
            cur.execute("""
                SELECT deportistas.*, grados.nombre AS grado_nombre
                FROM deportistas
                LEFT JOIN grados ON grados.id = deportistas.grado_id
                WHERE deportistas.deporte_id = %s
                ORDER BY deportistas.orden, deportistas.nombre
            """, (id,))
            jugadores = cur.fetchall()
    return render_template(
        'deporte_detalle.html', titulo=deporte['nombre'], deporte=deporte, equipos=equipos,
        niveles=_jugadores_por_grado(grados, jugadores), totalJugadores=len(jugadores),
        iconoDeporte=_icono_deporte(deporte['nombre']),
    )


NOMBRES_GRADO = {
    1: 'Primero', 2: 'Segundo', 3: 'Tercero', 4: 'Cuarto', 5: 'Quinto', 6: 'Sexto',
    7: 'Séptimo', 8: 'Octavo', 9: 'Noveno', 10: 'Décimo', 11: 'Once',
}


def _jugadores_por_grado(grados, jugadores):
    """Arma grado -> salones -> jugadores. Salen todos los salones creados en /admin/grados,
    aunque todavia no tengan jugadores; los jugadores sin curso van al final en 'Otros'."""
    por_salon = {}
    for j in jugadores:
        por_salon.setdefault(j['grado_id'], []).append(j)

    niveles = []
    for g in grados:
        if not niveles or niveles[-1]['nivel'] != g['nivel']:
            niveles.append({
                'nivel': g['nivel'],
                'etiqueta': f"{g['nivel']}°",
                'nombre': NOMBRES_GRADO.get(g['nivel'], f"Grado {g['nivel']}"),
                'salones': [],
            })
        niveles[-1]['salones'].append({'grado': g, 'nombre': g['nombre'], 'jugadores': por_salon.get(g['id'], [])})

    if por_salon.get(None):
        niveles.append({
            'nivel': None, 'etiqueta': '★', 'nombre': 'Otros',
            'salones': [{'grado': None, 'nombre': 'Sin curso', 'jugadores': por_salon[None]}],
        })

    for n in niveles:
        n['total'] = sum(len(s['jugadores']) for s in n['salones'])
    return niveles


def _icono_deporte(nombre):
    """Emoji del deporte para la esquina de las tarjetas."""
    nombre = (nombre or '').lower()
    for clave, icono in (
        ('fut', '⚽'), ('micro', '⚽'), ('balonc', '🏀'), ('basket', '🏀'), ('vole', '🏐'),
        ('balonm', '🤾'), ('badm', '🏸'), ('bádm', '🏸'), ('tenis', '🎾'), ('ajedrez', '♟️'),
        ('atlet', '🏃'), ('nata', '🏊'), ('beis', '⚾'),
    ):
        if clave in nombre:
            return icono
    return '🏅'


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


def _filas_piramide_icfes(resultados):
    """Los 10 mejores puntajes en forma de piramide: 1 arriba, luego 2, 3 y 4."""
    mejores = resultados[:10]
    filas = []
    inicio = 0
    tamanio = 1
    while inicio < len(mejores):
        filas.append(mejores[inicio:inicio + tamanio])
        inicio += tamanio
        tamanio += 1
    return filas


@public_bp.route('/icfes')
def icfes():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM icfes_resultados ORDER BY anio DESC, puntaje DESC, creado_en ASC')
            resultados = cur.fetchall()
    grupos = _agrupar_por_anio(resultados)
    for grupo in grupos:
        grupo['filas'] = _filas_piramide_icfes(grupo['resultados'])
    return render_template('icfes.html', titulo='Mejores ICFES', grupos=grupos)


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
    anio = request.args.get('anio', type=int)
    evento_id = request.args.get('evento', type=int)

    base = "FROM galeria_fotos WHERE visible = true AND (seccion IS NULL OR seccion <> 'inicio')"
    condiciones, valores = '', []
    if anio:
        condiciones += ' AND extract(year FROM fecha) = %s'
        valores.append(anio)
    if evento_id:
        condiciones += ' AND evento_id = %s'
        valores.append(evento_id)

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(f'SELECT * {base}{condiciones} ORDER BY fecha DESC, creado_en DESC', valores)
            fotos = cur.fetchall()
            cur.execute(f'SELECT DISTINCT extract(year FROM fecha)::int AS anio {base} ORDER BY anio DESC')
            anios = [r['anio'] for r in cur.fetchall()]
            cur.execute(
                f"""SELECT e.id, e.titulo, e.fecha FROM eventos e
                    WHERE e.id IN (SELECT evento_id {base} AND evento_id IS NOT NULL)
                    ORDER BY e.fecha DESC"""
            )
            eventos = cur.fetchall()
    return render_template(
        'galeria.html', titulo='Galeria', grupos=_agrupar_por_mes(fotos), total=len(fotos),
        anios=anios, eventos=eventos, anio=anio, evento_id=evento_id,
    )


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
