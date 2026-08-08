const pool = require('../../config/db');

exports.index = async (req, res) => {
    const deportes = await pool.query('SELECT * FROM deportes ORDER BY nombre');
    res.render('admin/deportes', { titulo: 'Admin · Deportes', deportes: deportes.rows });
};

exports.crear = async (req, res) => {
    const { nombre } = req.body;
    await pool.query('INSERT INTO deportes (nombre) VALUES ($1)', [nombre]);
    res.redirect('/admin/deportes');
};

exports.editarForm = async (req, res) => {
    const deporte = await pool.query('SELECT * FROM deportes WHERE id = $1', [req.params.id]);
    if (deporte.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/deportes-editar', { titulo: 'Admin · Editar deporte', deporte: deporte.rows[0] });
};

exports.editar = async (req, res) => {
    const { nombre } = req.body;
    await pool.query('UPDATE deportes SET nombre = $1 WHERE id = $2', [nombre, req.params.id]);
    res.redirect('/admin/deportes');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM deportes WHERE id = $1', [req.params.id]);
    res.redirect('/admin/deportes');
};
