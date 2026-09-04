const pool = require('../../config/db');

function hoyLocal() {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

const SECCIONES = {
    'inicio': 'Inicio (carrusel del encabezado)',
    'coheteria': 'Cohetería',
    'comite-ecologico': 'Comité Ecológico',
    'equipo-drones': 'Equipo de Drones',
    'equipo-desarrollo': 'Equipo de Desarrollo',
};

exports.index = async (req, res) => {
    const fotos = await pool.query(`
        SELECT galeria_fotos.*, eventos.titulo AS evento_titulo, noticias.titulo AS noticia_titulo,
            media_tecnica_categorias.nombre AS media_tecnica_nombre
        FROM galeria_fotos
        LEFT JOIN eventos ON eventos.id = galeria_fotos.evento_id
        LEFT JOIN noticias ON noticias.id = galeria_fotos.noticia_id
        LEFT JOIN media_tecnica_categorias ON media_tecnica_categorias.id = galeria_fotos.media_tecnica_categoria_id
        ORDER BY galeria_fotos.fecha DESC, galeria_fotos.creado_en DESC
    `);
    const eventos = await pool.query('SELECT id, titulo FROM eventos ORDER BY fecha DESC');
    const noticias = await pool.query('SELECT id, titulo FROM noticias ORDER BY fecha DESC');
    const categoriasMediaTecnica = await pool.query('SELECT id, nombre FROM media_tecnica_categorias ORDER BY orden, nombre');
    res.render('admin/fotos', {
        titulo: 'Admin · Galería',
        fotos: fotos.rows.map((f) => ({ ...f, seccion_nombre: SECCIONES[f.seccion] || null })),
        eventos: eventos.rows,
        noticias: noticias.rows,
        categoriasMediaTecnica: categoriasMediaTecnica.rows,
        secciones: SECCIONES,
    });
};

exports.crear = async (req, res) => {
    if (!req.files || req.files.length === 0) {
        return res.redirect('/admin/fotos');
    }
    const { titulo, evento_id, noticia_id, media_tecnica_categoria_id, seccion, fecha, orden } = req.body;

    for (const archivo of req.files) {
        const url = `/images/${archivo.filename}`;
        await pool.query(
            'INSERT INTO galeria_fotos (titulo, url, evento_id, noticia_id, media_tecnica_categoria_id, seccion, fecha, orden) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
            [titulo || null, url, evento_id || null, noticia_id || null, media_tecnica_categoria_id || null, seccion || null, fecha || hoyLocal(), orden || 1]
        );
    }

    res.redirect('/admin/fotos');
};

exports.editarLote = async (req, res) => {
    const idsRaw = req.body.ids;
    const ids = Array.isArray(idsRaw) ? idsRaw : (idsRaw ? [idsRaw] : []);
    if (ids.length === 0) {
        return res.redirect('/admin/fotos');
    }

    const { evento_lote, media_tecnica_categoria_lote, seccion_lote, fecha_lote, titulo_lote, orden_lote } = req.body;
    const cambios = [];
    const valores = [];
    let i = 1;

    if (evento_lote !== undefined && evento_lote !== '__no_cambiar__') {
        cambios.push(`evento_id = $${i++}`);
        valores.push(evento_lote || null);
    }
    if (media_tecnica_categoria_lote !== undefined && media_tecnica_categoria_lote !== '__no_cambiar__') {
        cambios.push(`media_tecnica_categoria_id = $${i++}`);
        valores.push(media_tecnica_categoria_lote || null);
    }
    if (seccion_lote !== undefined && seccion_lote !== '__no_cambiar__') {
        cambios.push(`seccion = $${i++}`);
        valores.push(seccion_lote || null);
    }
    if (fecha_lote) {
        cambios.push(`fecha = $${i++}`);
        valores.push(fecha_lote);
    }
    if (titulo_lote) {
        cambios.push(`titulo = $${i++}`);
        valores.push(titulo_lote);
    }
    if (orden_lote) {
        cambios.push(`orden = $${i++}`);
        valores.push(orden_lote);
    }

    if (cambios.length > 0) {
        valores.push(ids);
        await pool.query(
            `UPDATE galeria_fotos SET ${cambios.join(', ')} WHERE id = ANY($${i}::int[])`,
            valores
        );
    }

    res.redirect('/admin/fotos');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM galeria_fotos WHERE id = $1', [req.params.id]);
    res.redirect('/admin/fotos');
};

exports.toggleVisible = async (req, res) => {
    const r = await pool.query('UPDATE galeria_fotos SET visible = NOT visible WHERE id = $1 RETURNING visible', [req.params.id]);
    res.json({ visible: r.rows[0].visible });
};

exports.editarForm = async (req, res) => {
    const foto = await pool.query('SELECT * FROM galeria_fotos WHERE id = $1', [req.params.id]);
    if (foto.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    const eventos = await pool.query('SELECT id, titulo FROM eventos ORDER BY fecha DESC');
    const noticias = await pool.query('SELECT id, titulo FROM noticias ORDER BY fecha DESC');
    const categoriasMediaTecnica = await pool.query('SELECT id, nombre FROM media_tecnica_categorias ORDER BY orden, nombre');
    res.render('admin/fotos-editar', {
        titulo: 'Admin · Editar foto',
        foto: foto.rows[0],
        eventos: eventos.rows,
        noticias: noticias.rows,
        categoriasMediaTecnica: categoriasMediaTecnica.rows,
        secciones: SECCIONES,
    });
};

exports.editar = async (req, res) => {
    const { titulo, evento_id, noticia_id, media_tecnica_categoria_id, seccion, url_actual, fecha, orden } = req.body;
    const url = req.file ? `/images/${req.file.filename}` : url_actual;
    await pool.query(
        'UPDATE galeria_fotos SET titulo = $1, url = $2, evento_id = $3, noticia_id = $4, media_tecnica_categoria_id = $5, seccion = $6, fecha = $7, orden = $8 WHERE id = $9',
        [titulo || null, url, evento_id || null, noticia_id || null, media_tecnica_categoria_id || null, seccion || null, fecha || hoyLocal(), orden || 1, req.params.id]
    );
    res.redirect('/admin/fotos');
};
