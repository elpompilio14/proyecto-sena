const pool = require('../../config/db');

exports.index = async (req, res) => {
    const noticias = await pool.query('SELECT * FROM noticias ORDER BY fecha DESC');
    res.render('admin/noticias', { titulo: 'Admin · Noticias', noticias: noticias.rows });
};

exports.crear = async (req, res) => {
    const { titulo, contenido, fecha } = req.body;
    const imagen_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        `INSERT INTO noticias (titulo, contenido, fecha, imagen_url, creado_por)
         VALUES ($1, $2, $3, $4, $5)`,
        [titulo, contenido, fecha, imagen_url, req.session.usuario.id]
    );
    res.redirect('/admin/noticias');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM noticias WHERE id = $1', [req.params.id]);
    res.redirect('/admin/noticias');
};

exports.editarForm = async (req, res) => {
    const noticia = await pool.query('SELECT * FROM noticias WHERE id = $1', [req.params.id]);
    if (noticia.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/noticias-editar', { titulo: 'Admin · Editar noticia', noticia: noticia.rows[0] });
};

exports.editar = async (req, res) => {
    const { titulo, contenido, fecha, imagen_actual } = req.body;
    const imagen_url = req.file ? `/images/${req.file.filename}` : (imagen_actual || null);
    await pool.query(
        `UPDATE noticias SET titulo = $1, contenido = $2, fecha = $3, imagen_url = $4
         WHERE id = $5`,
        [titulo, contenido, fecha, imagen_url, req.params.id]
    );
    res.redirect('/admin/noticias');
};
