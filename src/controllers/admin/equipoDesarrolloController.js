const pool = require('../../config/db');

exports.index = async (req, res) => {
    const miembros = await pool.query('SELECT * FROM equipo_desarrollo ORDER BY nombre');
    res.render('admin/equipo-desarrollo', { titulo: 'Admin · Equipo de Desarrollo', miembros: miembros.rows });
};

exports.crear = async (req, res) => {
    const { nombre, rol } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        'INSERT INTO equipo_desarrollo (nombre, rol, foto_url) VALUES ($1, $2, $3)',
        [nombre, rol || null, foto_url]
    );
    res.redirect('/admin/equipo-desarrollo');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM equipo_desarrollo WHERE id = $1', [req.params.id]);
    res.redirect('/admin/equipo-desarrollo');
};

exports.editarForm = async (req, res) => {
    const miembro = await pool.query('SELECT * FROM equipo_desarrollo WHERE id = $1', [req.params.id]);
    if (miembro.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/equipo-desarrollo-editar', { titulo: 'Admin · Editar miembro', miembro: miembro.rows[0] });
};

exports.editar = async (req, res) => {
    const { nombre, rol, foto_actual } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : (foto_actual || null);
    await pool.query(
        'UPDATE equipo_desarrollo SET nombre = $1, rol = $2, foto_url = $3 WHERE id = $4',
        [nombre, rol || null, foto_url, req.params.id]
    );
    res.redirect('/admin/equipo-desarrollo');
};
