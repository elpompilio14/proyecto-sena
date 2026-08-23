const pool = require('../../config/db');

function hoyLocal() {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

exports.index = async (req, res) => {
    const fotos = await pool.query(`
        SELECT galeria_fotos.*, eventos.titulo AS evento_titulo, noticias.titulo AS noticia_titulo
        FROM galeria_fotos
        LEFT JOIN eventos ON eventos.id = galeria_fotos.evento_id
        LEFT JOIN noticias ON noticias.id = galeria_fotos.noticia_id
        ORDER BY galeria_fotos.fecha DESC, galeria_fotos.creado_en DESC
    `);
    const eventos = await pool.query('SELECT id, titulo FROM eventos ORDER BY fecha DESC');
    const noticias = await pool.query('SELECT id, titulo FROM noticias ORDER BY fecha DESC');
    res.render('admin/fotos', { titulo: 'Admin · Galería', fotos: fotos.rows, eventos: eventos.rows, noticias: noticias.rows });
};

exports.crear = async (req, res) => {
    if (!req.files || req.files.length === 0) {
        return res.redirect('/admin/fotos');
    }
    const { titulo, evento_id, noticia_id, fecha, orden } = req.body;

    for (const archivo of req.files) {
        const url = `/images/${archivo.filename}`;
        await pool.query(
            'INSERT INTO galeria_fotos (titulo, url, evento_id, noticia_id, fecha, orden) VALUES ($1, $2, $3, $4, $5, $6)',
            [titulo || null, url, evento_id || null, noticia_id || null, fecha || hoyLocal(), orden || 0]
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

    const { evento_lote, fecha_lote, titulo_lote } = req.body;
    const cambios = [];
    const valores = [];
    let i = 1;

    if (evento_lote !== undefined && evento_lote !== '__no_cambiar__') {
        cambios.push(`evento_id = $${i++}`);
        valores.push(evento_lote || null);
    }
    if (fecha_lote) {
        cambios.push(`fecha = $${i++}`);
        valores.push(fecha_lote);
    }
    if (titulo_lote) {
        cambios.push(`titulo = $${i++}`);
        valores.push(titulo_lote);
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

exports.editarForm = async (req, res) => {
    const foto = await pool.query('SELECT * FROM galeria_fotos WHERE id = $1', [req.params.id]);
    if (foto.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    const eventos = await pool.query('SELECT id, titulo FROM eventos ORDER BY fecha DESC');
    const noticias = await pool.query('SELECT id, titulo FROM noticias ORDER BY fecha DESC');
    res.render('admin/fotos-editar', { titulo: 'Admin · Editar foto', foto: foto.rows[0], eventos: eventos.rows, noticias: noticias.rows });
};

exports.editar = async (req, res) => {
    const { titulo, evento_id, noticia_id, url_actual, fecha, orden } = req.body;
    const url = req.file ? `/images/${req.file.filename}` : url_actual;
    await pool.query(
        'UPDATE galeria_fotos SET titulo = $1, url = $2, evento_id = $3, noticia_id = $4, fecha = $5, orden = $6 WHERE id = $7',
        [titulo || null, url, evento_id || null, noticia_id || null, fecha || hoyLocal(), orden || 0, req.params.id]
    );
    res.redirect('/admin/fotos');
};
