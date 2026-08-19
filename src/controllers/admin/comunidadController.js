const pool = require('../../config/db');

exports.index = async (req, res) => {
    const personas = await pool.query('SELECT * FROM comunidad_educativa ORDER BY nombre');
    res.render('admin/comunidad', { titulo: 'Admin · Comunidad Educativa', personas: personas.rows });
};

exports.crear = async (req, res) => {
    const { nombre, cargo } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        'INSERT INTO comunidad_educativa (nombre, cargo, foto_url) VALUES ($1, $2, $3)',
        [nombre, cargo || null, foto_url]
    );
    res.redirect('/admin/comunidad-educativa');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM comunidad_educativa WHERE id = $1', [req.params.id]);
    res.redirect('/admin/comunidad-educativa');
};

exports.editarForm = async (req, res) => {
    const persona = await pool.query('SELECT * FROM comunidad_educativa WHERE id = $1', [req.params.id]);
    if (persona.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/comunidad-editar', { titulo: 'Admin · Editar persona', persona: persona.rows[0] });
};

exports.editar = async (req, res) => {
    const { nombre, cargo, foto_actual } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : (foto_actual || null);
    await pool.query(
        'UPDATE comunidad_educativa SET nombre = $1, cargo = $2, foto_url = $3 WHERE id = $4',
        [nombre, cargo || null, foto_url, req.params.id]
    );
    res.redirect('/admin/comunidad-educativa');
};
