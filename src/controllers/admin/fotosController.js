const pool = require('../../config/db');

exports.index = async (req, res) => {
    const fotos = await pool.query(`
        SELECT galeria_fotos.*, eventos.titulo AS evento_titulo, noticias.titulo AS noticia_titulo
        FROM galeria_fotos
        LEFT JOIN eventos ON eventos.id = galeria_fotos.evento_id
        LEFT JOIN noticias ON noticias.id = galeria_fotos.noticia_id
        ORDER BY galeria_fotos.creado_en DESC
    `);
    const eventos = await pool.query('SELECT id, titulo FROM eventos ORDER BY fecha DESC');
    const noticias = await pool.query('SELECT id, titulo FROM noticias ORDER BY fecha DESC');
    res.render('admin/fotos', { titulo: 'Admin · Galería', fotos: fotos.rows, eventos: eventos.rows, noticias: noticias.rows });
};

exports.crear = async (req, res) => {
    if (!req.files || req.files.length === 0) {
        return res.redirect('/admin/fotos');
    }
    const { titulo, evento_id, noticia_id } = req.body;

    for (const archivo of req.files) {
        const url = `/images/${archivo.filename}`;
        await pool.query(
            'INSERT INTO galeria_fotos (titulo, url, evento_id, noticia_id) VALUES ($1, $2, $3, $4)',
            [titulo || null, url, evento_id || null, noticia_id || null]
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
    const { titulo, evento_id, noticia_id, url_actual } = req.body;
    const url = req.file ? `/images/${req.file.filename}` : url_actual;
    await pool.query(
        'UPDATE galeria_fotos SET titulo = $1, url = $2, evento_id = $3, noticia_id = $4 WHERE id = $5',
        [titulo || null, url, evento_id || null, noticia_id || null, req.params.id]
    );
    res.redirect('/admin/fotos');
};
