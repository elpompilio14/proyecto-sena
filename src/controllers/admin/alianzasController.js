const pool = require('../../config/db');

exports.index = async (req, res) => {
    const alianzas = await pool.query('SELECT * FROM alianzas ORDER BY nombre');
    res.render('admin/alianzas', { titulo: 'Admin · Alianzas', alianzas: alianzas.rows });
};

exports.crear = async (req, res) => {
    const { nombre, link_url } = req.body;
    const logo_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        'INSERT INTO alianzas (nombre, logo_url, link_url) VALUES ($1, $2, $3)',
        [nombre, logo_url, link_url || null]
    );
    res.redirect('/admin/alianzas');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM alianzas WHERE id = $1', [req.params.id]);
    res.redirect('/admin/alianzas');
};

exports.editarForm = async (req, res) => {
    const alianza = await pool.query('SELECT * FROM alianzas WHERE id = $1', [req.params.id]);
    if (alianza.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/alianzas-editar', { titulo: 'Admin · Editar alianza', alianza: alianza.rows[0] });
};

exports.editar = async (req, res) => {
    const { nombre, link_url, logo_actual } = req.body;
    const logo_url = req.file ? `/images/${req.file.filename}` : (logo_actual || null);
    await pool.query(
        'UPDATE alianzas SET nombre = $1, logo_url = $2, link_url = $3 WHERE id = $4',
        [nombre, logo_url, link_url || null, req.params.id]
    );
    res.redirect('/admin/alianzas');
};
