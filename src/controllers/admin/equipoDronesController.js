const pool = require('../../config/db');

exports.index = async (req, res) => {
    const miembros = await pool.query('SELECT * FROM equipo_drones ORDER BY orden, nombre');
    res.render('admin/equipo-drones', { titulo: 'Admin · Equipo de Drones', miembros: miembros.rows });
};

exports.crear = async (req, res) => {
    const { nombre, rol, orden, nivel } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        'INSERT INTO equipo_drones (nombre, rol, foto_url, orden, nivel) VALUES ($1, $2, $3, $4, $5)',
        [nombre, rol || null, foto_url, orden || 0, nivel || 'base']
    );
    res.redirect('/admin/equipo-drones');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM equipo_drones WHERE id = $1', [req.params.id]);
    res.redirect('/admin/equipo-drones');
};

exports.editarForm = async (req, res) => {
    const miembro = await pool.query('SELECT * FROM equipo_drones WHERE id = $1', [req.params.id]);
    if (miembro.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/equipo-drones-editar', { titulo: 'Admin · Editar miembro', miembro: miembro.rows[0] });
};

exports.editar = async (req, res) => {
    const { nombre, rol, foto_actual, orden, nivel } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : (foto_actual || null);
    await pool.query(
        'UPDATE equipo_drones SET nombre = $1, rol = $2, foto_url = $3, orden = $4, nivel = $5 WHERE id = $6',
        [nombre, rol || null, foto_url, orden || 0, nivel || 'base', req.params.id]
    );
    res.redirect('/admin/equipo-drones');
};
