const pool = require('../config/db');

function agruparPorNivel(filas) {
    const grupos = { punta: [], medio: [], base: [] };
    filas.forEach((r) => {
        const nivel = ['punta', 'medio', 'base'].includes(r.nivel) ? r.nivel : 'base';
        grupos[nivel].push(r);
    });
    return grupos;
}

// Version recortada de un grupo (piramide) para mostrar como vista previa en el inicio:
// si hay punta, muestra la punta completa + hasta 3 personas mas; si no hay punta, muestra solo las primeras 3.
function recortarParaInicio(grupos) {
    const resto = grupos.medio.concat(grupos.base);
    if (grupos.punta.length > 0) {
        return { punta: grupos.punta, medio: resto.slice(0, 3), base: [] };
    }
    return { punta: [], medio: resto.slice(0, 3), base: [] };
}

exports.home = async (req, res) => {
    const eventos = await pool.query(
        'SELECT * FROM eventos ORDER BY fecha DESC LIMIT 6'
    );
    const noticias = await pool.query(
        'SELECT * FROM noticias ORDER BY fecha DESC LIMIT 3'
    );
    const icfesResultados = await pool.query(`
        SELECT * FROM icfes_resultados
        WHERE anio = (SELECT MAX(anio) FROM icfes_resultados)
        ORDER BY puntaje DESC, creado_en ASC
        LIMIT 3
    `);
    const gobiernoEscolar = await pool.query('SELECT * FROM gobierno_escolar ORDER BY orden, nombre');
    const equipoDesarrollo = await pool.query('SELECT * FROM equipo_desarrollo ORDER BY orden, nombre');
    const comiteEcologico = await pool.query('SELECT * FROM comite_ecologico ORDER BY orden, nombre');
    const equipoDrones = await pool.query('SELECT * FROM equipo_drones ORDER BY orden, nombre');
    const coheteria = await pool.query('SELECT * FROM coheteria ORDER BY orden, nombre');
    const info = await pool.query('SELECT himno_url, fondo_url FROM institucion_info ORDER BY id LIMIT 1');
    const heroFotos = await pool.query(
        "SELECT url FROM galeria_fotos WHERE seccion = 'inicio' AND visible = true ORDER BY orden, id"
    );
    res.render('home', {
        titulo: 'Inicio',
        eventos: eventos.rows,
        noticias: noticias.rows,
        icfesResultados: icfesResultados.rows,
        icfesAnio: icfesResultados.rows[0] ? icfesResultados.rows[0].anio : null,
        gobiernoEscolar: recortarParaInicio(agruparPorNivel(gobiernoEscolar.rows)),
        equipoDesarrollo: recortarParaInicio(agruparPorNivel(equipoDesarrollo.rows)),
        comiteEcologico: recortarParaInicio(agruparPorNivel(comiteEcologico.rows)),
        equipoDrones: recortarParaInicio(agruparPorNivel(equipoDrones.rows)),
        coheteria: recortarParaInicio(agruparPorNivel(coheteria.rows)),
        himnoUrl: info.rows[0] ? info.rows[0].himno_url : null,
        fondoUrl: info.rows[0] ? info.rows[0].fondo_url : null,
        heroImagenes: heroFotos.rows.map((f) => f.url),
    });
};

exports.gobiernoEscolar = async (req, res) => {
    const miembros = await pool.query('SELECT * FROM gobierno_escolar ORDER BY orden, nombre');
    res.render('gobierno-escolar', { titulo: 'Gobierno Escolar', grupos: agruparPorNivel(miembros.rows) });
};

exports.equipoDesarrollo = async (req, res) => {
    const miembros = await pool.query('SELECT * FROM equipo_desarrollo ORDER BY orden, nombre');
    const info = await pool.query('SELECT equipo_desarrollo_texto, equipo_desarrollo_portada_url FROM institucion_info ORDER BY id LIMIT 1');
    const fotos = await pool.query("SELECT * FROM galeria_fotos WHERE seccion = 'equipo-desarrollo' AND visible = true ORDER BY orden, creado_en");
    res.render('equipo-desarrollo', {
        titulo: 'Equipo de Desarrollo',
        grupos: agruparPorNivel(miembros.rows),
        texto: info.rows[0] ? info.rows[0].equipo_desarrollo_texto : null,
        portada: info.rows[0] ? info.rows[0].equipo_desarrollo_portada_url : null,
        fotos: fotos.rows,
    });
};

exports.comiteEcologico = async (req, res) => {
    const miembros = await pool.query('SELECT * FROM comite_ecologico ORDER BY orden, nombre');
    const info = await pool.query('SELECT comite_ecologico_texto, comite_ecologico_portada_url FROM institucion_info ORDER BY id LIMIT 1');
    const fotos = await pool.query("SELECT * FROM galeria_fotos WHERE seccion = 'comite-ecologico' AND visible = true ORDER BY orden, creado_en");
    res.render('comite-ecologico', {
        titulo: 'Comité Ecológico',
        grupos: agruparPorNivel(miembros.rows),
        texto: info.rows[0] ? info.rows[0].comite_ecologico_texto : null,
        portada: info.rows[0] ? info.rows[0].comite_ecologico_portada_url : null,
        fotos: fotos.rows,
    });
};

exports.equipoDrones = async (req, res) => {
    const miembros = await pool.query('SELECT * FROM equipo_drones ORDER BY orden, nombre');
    const info = await pool.query('SELECT equipo_drones_texto, equipo_drones_portada_url FROM institucion_info ORDER BY id LIMIT 1');
    const fotos = await pool.query("SELECT * FROM galeria_fotos WHERE seccion = 'equipo-drones' AND visible = true ORDER BY orden, creado_en");
    res.render('equipo-drones', {
        titulo: 'Equipo de Drones',
        grupos: agruparPorNivel(miembros.rows),
        texto: info.rows[0] ? info.rows[0].equipo_drones_texto : null,
        portada: info.rows[0] ? info.rows[0].equipo_drones_portada_url : null,
        fotos: fotos.rows,
    });
};

exports.coheteria = async (req, res) => {
    const miembros = await pool.query('SELECT * FROM coheteria ORDER BY orden, nombre');
    const info = await pool.query('SELECT coheteria_texto, coheteria_portada_url FROM institucion_info ORDER BY id LIMIT 1');
    const fotos = await pool.query("SELECT * FROM galeria_fotos WHERE seccion = 'coheteria' AND visible = true ORDER BY orden, creado_en");
    res.render('coheteria', {
        titulo: 'Cohetería',
        grupos: agruparPorNivel(miembros.rows),
        texto: info.rows[0] ? info.rows[0].coheteria_texto : null,
        portada: info.rows[0] ? info.rows[0].coheteria_portada_url : null,
        fotos: fotos.rows,
    });
};

exports.eventos = async (req, res) => {
    const eventos = await pool.query(
        'SELECT * FROM eventos ORDER BY fecha DESC'
    );
    res.render('eventos', { titulo: 'Eventos', eventos: eventos.rows });
};

exports.eventoDetalle = async (req, res) => {
    const evento = await pool.query('SELECT * FROM eventos WHERE id = $1', [req.params.id]);

    if (evento.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }

    const fotos = await pool.query(
        'SELECT * FROM galeria_fotos WHERE evento_id = $1 AND visible = true ORDER BY orden, creado_en',
        [req.params.id]
    );

    res.render('evento-detalle', {
        titulo: evento.rows[0].titulo,
        evento: evento.rows[0],
        fotos: fotos.rows,
    });
};

exports.gruposEstudiantiles = async (req, res) => {
    const grupos = await pool.query('SELECT * FROM grupos_estudiantiles ORDER BY nombre');
    res.render('grupos-estudiantiles', { titulo: 'Grupos y Semilleros', grupos: grupos.rows });
};

exports.deportes = async (req, res) => {
    const deportes = await pool.query('SELECT * FROM deportes ORDER BY nombre');
    const equipos = await pool.query(`
        SELECT equipos.*, deportes.nombre AS deporte_nombre
        FROM equipos
        JOIN deportes ON deportes.id = equipos.deporte_id
        ORDER BY deportes.nombre, equipos.nombre
    `);
    res.render('deportes', { titulo: 'Equipos deportivos', deportes: deportes.rows, equipos: equipos.rows });
};

exports.deporteDetalle = async (req, res) => {
    const deporte = await pool.query('SELECT * FROM deportes WHERE id = $1', [req.params.id]);
    if (deporte.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    const equipos = await pool.query(
        'SELECT * FROM equipos WHERE deporte_id = $1 ORDER BY nombre',
        [req.params.id]
    );
    res.render('deporte-detalle', { titulo: deporte.rows[0].nombre, deporte: deporte.rows[0], equipos: equipos.rows });
};

exports.campeonatos = async (req, res) => {
    const campeonatos = await pool.query(`
        SELECT campeonatos.*, deportes.nombre AS deporte_nombre
        FROM campeonatos
        JOIN deportes ON deportes.id = campeonatos.deporte_id
        ORDER BY campeonatos.fecha_inicio DESC
    `);
    res.render('campeonatos', { titulo: 'Intercursos', campeonatos: campeonatos.rows });
};

exports.campeonatoDetalle = async (req, res) => {
    const campeonato = await pool.query(`
        SELECT campeonatos.*, deportes.nombre AS deporte_nombre
        FROM campeonatos
        JOIN deportes ON deportes.id = campeonatos.deporte_id
        WHERE campeonatos.id = $1
    `, [req.params.id]);

    if (campeonato.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }

    const resultados = await pool.query(`
        SELECT resultados.*, el.nombre AS equipo_local_nombre, ev.nombre AS equipo_visitante_nombre
        FROM resultados
        JOIN equipos el ON el.id = resultados.equipo_local_id
        JOIN equipos ev ON ev.id = resultados.equipo_visitante_id
        WHERE resultados.campeonato_id = $1
        ORDER BY resultados.fecha
    `, [req.params.id]);

    res.render('campeonato-detalle', {
        titulo: campeonato.rows[0].nombre,
        campeonato: campeonato.rows[0],
        resultados: resultados.rows,
    });
};

exports.mejoresPuestos = async (req, res) => {
    const puestos = await pool.query(`
        SELECT mejores_puestos.*, estudiantes.nombres, estudiantes.apellidos, grados.nombre AS grado_nombre
        FROM mejores_puestos
        JOIN estudiantes ON estudiantes.id = mejores_puestos.estudiante_id
        JOIN grados ON grados.id = mejores_puestos.grado_id
        ORDER BY grados.nivel, mejores_puestos.periodo DESC, mejores_puestos.puesto
    `);
    res.render('mejores-puestos', { titulo: 'Puestos de honor', puestos: puestos.rows });
};

exports.alianzas = async (req, res) => {
    const alianzas = await pool.query('SELECT * FROM alianzas ORDER BY nombre');
    res.render('alianzas', { titulo: 'Alianzas', alianzas: alianzas.rows });
};

function agruparPorAnio(filas) {
    const grupos = [];
    let grupoActual = null;

    filas.forEach((r) => {
        if (!grupoActual || grupoActual.anio !== r.anio) {
            grupoActual = { anio: r.anio, resultados: [] };
            grupos.push(grupoActual);
        }
        grupoActual.resultados.push(r);
    });

    return grupos;
}

exports.icfes = async (req, res) => {
    const resultados = await pool.query('SELECT * FROM icfes_resultados ORDER BY anio DESC, puntaje DESC');
    res.render('icfes', { titulo: 'Mejores ICFES', grupos: agruparPorAnio(resultados.rows) });
};

const MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];

function agruparPorMes(filas) {
    const grupos = [];
    let grupoActual = null;

    filas.forEach((foto) => {
        const fecha = new Date(foto.fecha);
        const clave = `${fecha.getFullYear()}-${fecha.getMonth()}`;

        if (!grupoActual || grupoActual.clave !== clave) {
            const mes = MESES[fecha.getMonth()];
            grupoActual = {
                clave,
                etiqueta: `${mes.charAt(0).toUpperCase()}${mes.slice(1)} ${fecha.getFullYear()}`,
                fotos: [],
            };
            grupos.push(grupoActual);
        }
        grupoActual.fotos.push(foto);
    });

    return grupos;
}

exports.galeria = async (req, res) => {
    const fotos = await pool.query(
        'SELECT * FROM galeria_fotos WHERE visible = true ORDER BY fecha DESC, creado_en DESC'
    );
    res.render('galeria', { titulo: 'Galeria', grupos: agruparPorMes(fotos.rows) });
};

exports.institucion = async (req, res) => {
    const info = await pool.query('SELECT * FROM institucion_info ORDER BY id LIMIT 1');
    res.render('institucion', { titulo: 'Institución', info: info.rows[0] || null });
};

exports.articulado = async (req, res) => {
    const info = await pool.query('SELECT articulado_texto FROM institucion_info ORDER BY id LIMIT 1');
    const categorias = await pool.query('SELECT * FROM media_tecnica_categorias ORDER BY orden, nombre');
    res.render('articulado', {
        titulo: 'Articulado',
        texto: info.rows[0] ? info.rows[0].articulado_texto : null,
        categorias: categorias.rows,
    });
};

exports.mediaTecnicaDetalle = async (req, res) => {
    const categoria = await pool.query('SELECT * FROM media_tecnica_categorias WHERE id = $1', [req.params.id]);
    if (categoria.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    const fotos = await pool.query(
        'SELECT * FROM galeria_fotos WHERE media_tecnica_categoria_id = $1 AND visible = true ORDER BY orden, creado_en',
        [req.params.id]
    );
    res.render('media-tecnica-detalle', { titulo: categoria.rows[0].nombre, categoria: categoria.rows[0], fotos: fotos.rows });
};

exports.investigacion = async (req, res) => {
    const info = await pool.query('SELECT investigacion_texto FROM institucion_info ORDER BY id LIMIT 1');
    res.render('investigacion', { titulo: 'Investigación', texto: info.rows[0] ? info.rows[0].investigacion_texto : null });
};

exports.comunidadEducativa = async (req, res) => {
    const directivos = await pool.query("SELECT * FROM comunidad_educativa WHERE categoria IN ('rectoria', 'coordinacion') ORDER BY orden, nombre");
    const docentesPreview = await pool.query("SELECT * FROM comunidad_educativa WHERE categoria = 'docente' ORDER BY orden, nombre LIMIT 4");
    const totalDocentes = await pool.query("SELECT COUNT(*) FROM comunidad_educativa WHERE categoria = 'docente'");

    res.render('comunidad-educativa', {
        titulo: 'Comunidad Educativa',
        directivos: agruparPorNivel(directivos.rows),
        docentesPreview: docentesPreview.rows,
        totalDocentes: parseInt(totalDocentes.rows[0].count, 10),
    });
};

exports.docentes = async (req, res) => {
    const docentes = await pool.query("SELECT * FROM comunidad_educativa WHERE categoria = 'docente' ORDER BY orden, nombre");
    const areas = [...new Set(docentes.rows.map((d) => d.area).filter(Boolean))];
    const materias = new Set(docentes.rows.map((d) => d.materia).filter(Boolean));
    const aniosCombinados = docentes.rows.reduce((total, d) => total + (d.anios_experiencia || 0), 0);

    res.render('comunidad-docentes', {
        titulo: 'Nuestro Cuerpo de Docentes',
        docentes: docentes.rows,
        areas,
        totalAsignaturas: materias.size,
        aniosCombinados,
    });
};

exports.himno = async (req, res) => {
    const info = await pool.query('SELECT himno_url, himno_letra FROM institucion_info ORDER BY id LIMIT 1');
    res.render('himno', {
        titulo: 'Himno Escolar',
        himnoUrl: info.rows[0] ? info.rows[0].himno_url : null,
        himnoLetra: info.rows[0] ? info.rows[0].himno_letra : null,
    });
};

exports.noticias = async (req, res) => {
    const noticias = await pool.query('SELECT * FROM noticias ORDER BY fecha DESC');
    res.render('noticias', { titulo: 'Noticias', noticias: noticias.rows });
};

exports.noticiaDetalle = async (req, res) => {
    const noticia = await pool.query('SELECT * FROM noticias WHERE id = $1', [req.params.id]);

    if (noticia.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }

    const fotos = await pool.query(
        'SELECT * FROM galeria_fotos WHERE noticia_id = $1 AND visible = true ORDER BY orden, creado_en',
        [req.params.id]
    );

    res.render('noticia-detalle', {
        titulo: noticia.rows[0].titulo,
        noticia: noticia.rows[0],
        fotos: fotos.rows,
    });
};

exports.contactoForm = (req, res) => {
    res.render('contacto', { titulo: 'Contacto', enviado: false, error: null });
};

exports.contacto = async (req, res) => {
    const { nombre, apellido, email, mensaje } = req.body;

    if (!nombre || !email || !mensaje) {
        return res.status(400).render('contacto', {
            titulo: 'Contacto',
            enviado: false,
            error: 'Todos los campos son obligatorios',
        });
    }

    await pool.query(
        'INSERT INTO mensajes_contacto (nombre, apellido, email, mensaje) VALUES ($1, $2, $3, $4)',
        [nombre, apellido || null, email, mensaje]
    );

    res.render('contacto', { titulo: 'Contacto', enviado: true, error: null });
};
