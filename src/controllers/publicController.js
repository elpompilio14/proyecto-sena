const pool = require('../config/db');

exports.home = async (req, res) => {
    const eventos = await pool.query(
        'SELECT * FROM eventos ORDER BY fecha DESC LIMIT 6'
    );
    const noticias = await pool.query(
        'SELECT * FROM noticias ORDER BY fecha DESC LIMIT 3'
    );
    const info = await pool.query('SELECT himno_url, fondo_url FROM institucion_info ORDER BY id LIMIT 1');
    res.render('home', {
        titulo: 'Inicio',
        eventos: eventos.rows,
        noticias: noticias.rows,
        himnoUrl: info.rows[0] ? info.rows[0].himno_url : null,
        fondoUrl: info.rows[0] ? info.rows[0].fondo_url : null,
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
        'SELECT * FROM galeria_fotos WHERE evento_id = $1 ORDER BY creado_en',
        [req.params.id]
    );

    res.render('evento-detalle', {
        titulo: evento.rows[0].titulo,
        evento: evento.rows[0],
        fotos: fotos.rows,
    });
};

exports.deportes = async (req, res) => {
    const equipos = await pool.query(`
        SELECT equipos.*, deportes.nombre AS deporte_nombre
        FROM equipos
        JOIN deportes ON deportes.id = equipos.deporte_id
        ORDER BY deportes.nombre, equipos.nombre
    `);
    res.render('deportes', { titulo: 'Equipos deportivos', equipos: equipos.rows });
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

exports.galeria = async (req, res) => {
    const fotos = await pool.query(
        'SELECT * FROM galeria_fotos ORDER BY creado_en DESC'
    );
    res.render('galeria', { titulo: 'Galeria', fotos: fotos.rows });
};

exports.institucion = async (req, res) => {
    const info = await pool.query('SELECT * FROM institucion_info ORDER BY id LIMIT 1');
    res.render('institucion', { titulo: 'Institución', info: info.rows[0] || null });
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
        'SELECT * FROM galeria_fotos WHERE noticia_id = $1 ORDER BY creado_en',
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
    const { nombre, email, mensaje } = req.body;

    if (!nombre || !email || !mensaje) {
        return res.status(400).render('contacto', {
            titulo: 'Contacto',
            enviado: false,
            error: 'Todos los campos son obligatorios',
        });
    }

    await pool.query(
        'INSERT INTO mensajes_contacto (nombre, email, mensaje) VALUES ($1, $2, $3)',
        [nombre, email, mensaje]
    );

    res.render('contacto', { titulo: 'Contacto', enviado: true, error: null });
};
