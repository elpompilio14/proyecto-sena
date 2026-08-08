const pool = require('../../config/db');

exports.index = async (req, res) => {
    const campeonatos = await pool.query(`
        SELECT campeonatos.*, deportes.nombre AS deporte_nombre
        FROM campeonatos
        JOIN deportes ON deportes.id = campeonatos.deporte_id
        ORDER BY campeonatos.fecha_inicio DESC
    `);
    const deportes = await pool.query('SELECT * FROM deportes ORDER BY nombre');
    res.render('admin/campeonatos', { titulo: 'Admin · Campeonatos', campeonatos: campeonatos.rows, deportes: deportes.rows });
};

exports.crear = async (req, res) => {
    const { nombre, deporte_id, fecha_inicio, fecha_fin, descripcion } = req.body;
    await pool.query(
        `INSERT INTO campeonatos (nombre, deporte_id, fecha_inicio, fecha_fin, descripcion)
         VALUES ($1, $2, $3, $4, $5)`,
        [nombre, deporte_id, fecha_inicio || null, fecha_fin || null, descripcion || null]
    );
    res.redirect('/admin/campeonatos');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM campeonatos WHERE id = $1', [req.params.id]);
    res.redirect('/admin/campeonatos');
};

exports.editarForm = async (req, res) => {
    const campeonato = await pool.query('SELECT * FROM campeonatos WHERE id = $1', [req.params.id]);
    if (campeonato.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    const deportes = await pool.query('SELECT * FROM deportes ORDER BY nombre');
    res.render('admin/campeonatos-editar', { titulo: 'Admin · Editar campeonato', campeonato: campeonato.rows[0], deportes: deportes.rows });
};

exports.editar = async (req, res) => {
    const { nombre, deporte_id, fecha_inicio, fecha_fin, descripcion } = req.body;
    await pool.query(
        `UPDATE campeonatos SET nombre = $1, deporte_id = $2, fecha_inicio = $3, fecha_fin = $4, descripcion = $5
         WHERE id = $6`,
        [nombre, deporte_id, fecha_inicio || null, fecha_fin || null, descripcion || null, req.params.id]
    );
    res.redirect('/admin/campeonatos');
};
