const pool = require('../../config/db');

exports.index = async (req, res) => {
    const grados = await pool.query('SELECT * FROM grados ORDER BY nivel, nombre');
    res.render('admin/grados', { titulo: 'Admin · Grados', grados: grados.rows });
};

exports.crear = async (req, res) => {
    const { nombre, nivel } = req.body;
    await pool.query('INSERT INTO grados (nombre, nivel) VALUES ($1, $2)', [nombre, nivel]);
    res.redirect('/admin/grados');
};

exports.editarForm = async (req, res) => {
    const grado = await pool.query('SELECT * FROM grados WHERE id = $1', [req.params.id]);
    if (grado.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/grados-editar', { titulo: 'Admin · Editar grado', grado: grado.rows[0] });
};

exports.editar = async (req, res) => {
    const { nombre, nivel } = req.body;
    await pool.query('UPDATE grados SET nombre = $1, nivel = $2 WHERE id = $3', [nombre, nivel, req.params.id]);
    res.redirect('/admin/grados');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM grados WHERE id = $1', [req.params.id]);
    res.redirect('/admin/grados');
};
