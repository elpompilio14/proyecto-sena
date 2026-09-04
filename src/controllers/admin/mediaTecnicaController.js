const pool = require('../../config/db');

exports.index = async (req, res) => {
    const categorias = await pool.query('SELECT * FROM media_tecnica_categorias ORDER BY orden, nombre');
    res.render('admin/media-tecnica', { titulo: 'Admin · Media Técnica', categorias: categorias.rows });
};

exports.crear = async (req, res) => {
    const { nombre, descripcion, orden } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        'INSERT INTO media_tecnica_categorias (nombre, imagen_url, descripcion, orden) VALUES ($1, $2, $3, $4)',
        [nombre, foto_url, descripcion || null, orden || 0]
    );
    res.redirect('/admin/media-tecnica');
};

exports.editarForm = async (req, res) => {
    const categoria = await pool.query('SELECT * FROM media_tecnica_categorias WHERE id = $1', [req.params.id]);
    if (categoria.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/media-tecnica-editar', { titulo: 'Admin · Editar categoría', categoria: categoria.rows[0] });
};

exports.editar = async (req, res) => {
    const { nombre, descripcion, orden, imagen_actual } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : (imagen_actual || null);
    await pool.query(
        'UPDATE media_tecnica_categorias SET nombre = $1, imagen_url = $2, descripcion = $3, orden = $4 WHERE id = $5',
        [nombre, foto_url, descripcion || null, orden || 0, req.params.id]
    );
    res.redirect('/admin/media-tecnica');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM media_tecnica_categorias WHERE id = $1', [req.params.id]);
    res.redirect('/admin/media-tecnica');
};

exports.toggleVisible = async (req, res) => {
    const r = await pool.query('UPDATE media_tecnica_categorias SET visible = NOT visible WHERE id = $1 RETURNING visible', [req.params.id]);
    res.json({ visible: r.rows[0].visible });
};
