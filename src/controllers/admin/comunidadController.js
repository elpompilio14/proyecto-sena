const pool = require('../../config/db');

exports.index = async (req, res) => {
    const personas = await pool.query(`
        SELECT * FROM comunidad_educativa
        ORDER BY CASE categoria WHEN 'rectoria' THEN 1 WHEN 'coordinacion' THEN 2 ELSE 3 END, orden, nombre
    `);
    res.render('admin/comunidad', { titulo: 'Admin · Comunidad Educativa', personas: personas.rows });
};

exports.crear = async (req, res) => {
    const { nombre, cargo, categoria, area, materia, anios_experiencia, descripcion, orden, nivel } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        `INSERT INTO comunidad_educativa (nombre, cargo, categoria, area, materia, anios_experiencia, descripcion, foto_url, orden, nivel)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)`,
        [nombre, cargo || null, categoria || 'docente', area || null, materia || null,
            anios_experiencia || null, descripcion || null, foto_url, orden || 0, nivel || 'base']
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
    const { nombre, cargo, categoria, area, materia, anios_experiencia, descripcion, foto_actual, orden, nivel } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : (foto_actual || null);
    await pool.query(
        `UPDATE comunidad_educativa
         SET nombre = $1, cargo = $2, categoria = $3, area = $4, materia = $5,
             anios_experiencia = $6, descripcion = $7, foto_url = $8, orden = $9, nivel = $10
         WHERE id = $11`,
        [nombre, cargo || null, categoria || 'docente', area || null, materia || null,
            anios_experiencia || null, descripcion || null, foto_url, orden || 0, nivel || 'base', req.params.id]
    );
    res.redirect('/admin/comunidad-educativa');
};
