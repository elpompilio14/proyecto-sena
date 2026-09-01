const pool = require('../../config/db');

exports.index = async (req, res) => {
    const miembros = await pool.query('SELECT * FROM gobierno_escolar ORDER BY orden, nombre');
    res.render('admin/gobierno-escolar', { titulo: 'Admin · Gobierno Escolar', miembros: miembros.rows });
};

exports.crear = async (req, res) => {
    const { nombre, rol, orden, nivel } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        'INSERT INTO gobierno_escolar (nombre, rol, foto_url, orden, nivel) VALUES ($1, $2, $3, $4, $5)',
        [nombre, rol || null, foto_url, orden || 0, nivel || 'base']
    );
    res.redirect('/admin/gobierno-escolar');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM gobierno_escolar WHERE id = $1', [req.params.id]);
    res.redirect('/admin/gobierno-escolar');
};

exports.toggleVisible = async (req, res) => {
    const r = await pool.query('UPDATE gobierno_escolar SET visible = NOT visible WHERE id = $1 RETURNING visible', [req.params.id]);
    res.json({ visible: r.rows[0].visible });
};

exports.editarForm = async (req, res) => {
    const miembro = await pool.query('SELECT * FROM gobierno_escolar WHERE id = $1', [req.params.id]);
    if (miembro.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/gobierno-escolar-editar', { titulo: 'Admin · Editar miembro', miembro: miembro.rows[0] });
};

exports.editar = async (req, res) => {
    const { nombre, rol, foto_actual, orden, nivel } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : (foto_actual || null);
    await pool.query(
        'UPDATE gobierno_escolar SET nombre = $1, rol = $2, foto_url = $3, orden = $4, nivel = $5 WHERE id = $6',
        [nombre, rol || null, foto_url, orden || 0, nivel || 'base', req.params.id]
    );
    res.redirect('/admin/gobierno-escolar');
};
