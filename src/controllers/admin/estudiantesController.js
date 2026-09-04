const pool = require('../../config/db');

exports.index = async (req, res) => {
    const estudiantes = await pool.query(`
        SELECT estudiantes.*, grados.nombre AS grado_nombre
        FROM estudiantes
        LEFT JOIN grados ON grados.id = estudiantes.grado_id
        ORDER BY estudiantes.apellidos, estudiantes.nombres
    `);
    const grados = await pool.query('SELECT * FROM grados ORDER BY nivel, nombre');
    res.render('admin/estudiantes', { titulo: 'Admin · Estudiantes', estudiantes: estudiantes.rows, grados: grados.rows });
};

exports.crear = async (req, res) => {
    const { nombres, apellidos, grado_id } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        'INSERT INTO estudiantes (nombres, apellidos, grado_id, foto_url) VALUES ($1, $2, $3, $4)',
        [nombres, apellidos, grado_id || null, foto_url]
    );
    res.redirect('/admin/estudiantes');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM estudiantes WHERE id = $1', [req.params.id]);
    res.redirect('/admin/estudiantes');
};

exports.editarForm = async (req, res) => {
    const estudiante = await pool.query('SELECT * FROM estudiantes WHERE id = $1', [req.params.id]);
    if (estudiante.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    const grados = await pool.query('SELECT * FROM grados ORDER BY nivel, nombre');
    res.render('admin/estudiantes-editar', { titulo: 'Admin · Editar estudiante', estudiante: estudiante.rows[0], grados: grados.rows });
};

exports.editar = async (req, res) => {
    const { nombres, apellidos, grado_id, foto_actual } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : (foto_actual || null);
    await pool.query(
        'UPDATE estudiantes SET nombres = $1, apellidos = $2, grado_id = $3, foto_url = $4 WHERE id = $5',
        [nombres, apellidos, grado_id || null, foto_url, req.params.id]
    );
    res.redirect('/admin/estudiantes');
};
