const pool = require('../../config/db');

exports.index = async (req, res) => {
    const equipos = await pool.query(`
        SELECT equipos.*, deportes.nombre AS deporte_nombre
        FROM equipos
        JOIN deportes ON deportes.id = equipos.deporte_id
        ORDER BY deportes.nombre, equipos.nombre
    `);
    const deportes = await pool.query('SELECT * FROM deportes ORDER BY nombre');
    res.render('admin/equipos', { titulo: 'Admin · Equipos', equipos: equipos.rows, deportes: deportes.rows });
};

exports.crear = async (req, res) => {
    const { nombre, deporte_id, categoria, entrenador, descripcion } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        `INSERT INTO equipos (nombre, deporte_id, categoria, entrenador, foto_url, descripcion)
         VALUES ($1, $2, $3, $4, $5, $6)`,
        [nombre, deporte_id, categoria || null, entrenador || null, foto_url, descripcion || null]
    );
    res.redirect('/admin/equipos');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM equipos WHERE id = $1', [req.params.id]);
    res.redirect('/admin/equipos');
};

exports.toggleVisible = async (req, res) => {
    const r = await pool.query('UPDATE equipos SET visible = NOT visible WHERE id = $1 RETURNING visible', [req.params.id]);
    res.json({ visible: r.rows[0].visible });
};

exports.editarForm = async (req, res) => {
    const equipo = await pool.query('SELECT * FROM equipos WHERE id = $1', [req.params.id]);
    if (equipo.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    const deportes = await pool.query('SELECT * FROM deportes ORDER BY nombre');
    res.render('admin/equipos-editar', { titulo: 'Admin · Editar equipo', equipo: equipo.rows[0], deportes: deportes.rows });
};

exports.editar = async (req, res) => {
    const { nombre, deporte_id, categoria, entrenador, descripcion, foto_actual } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : (foto_actual || null);
    await pool.query(
        `UPDATE equipos SET nombre = $1, deporte_id = $2, categoria = $3, entrenador = $4, foto_url = $5, descripcion = $6
         WHERE id = $7`,
        [nombre, deporte_id, categoria || null, entrenador || null, foto_url, descripcion || null, req.params.id]
    );
    res.redirect('/admin/equipos');
};
