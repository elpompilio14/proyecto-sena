const pool = require('../../config/db');

exports.index = async (req, res) => {
    const eventos = await pool.query('SELECT * FROM eventos ORDER BY fecha DESC');
    res.render('admin/eventos', { titulo: 'Admin · Eventos', eventos: eventos.rows });
};

exports.crear = async (req, res) => {
    const { titulo, descripcion, fecha } = req.body;
    const imagen_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        `INSERT INTO eventos (titulo, descripcion, fecha, imagen_url, creado_por)
         VALUES ($1, $2, $3, $4, $5)`,
        [titulo, descripcion, fecha, imagen_url, req.session.usuario.id]
    );
    res.redirect('/admin/eventos');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM eventos WHERE id = $1', [req.params.id]);
    res.redirect('/admin/eventos');
};

exports.toggleVisible = async (req, res) => {
    const r = await pool.query('UPDATE eventos SET visible = NOT visible WHERE id = $1 RETURNING visible', [req.params.id]);
    res.json({ visible: r.rows[0].visible });
};

exports.editarForm = async (req, res) => {
    const evento = await pool.query('SELECT * FROM eventos WHERE id = $1', [req.params.id]);
    if (evento.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/eventos-editar', { titulo: 'Admin · Editar evento', evento: evento.rows[0] });
};

exports.editar = async (req, res) => {
    const { titulo, descripcion, fecha, imagen_actual } = req.body;
    const imagen_url = req.file ? `/images/${req.file.filename}` : (imagen_actual || null);
    await pool.query(
        `UPDATE eventos SET titulo = $1, descripcion = $2, fecha = $3, imagen_url = $4
         WHERE id = $5`,
        [titulo, descripcion, fecha, imagen_url, req.params.id]
    );
    res.redirect('/admin/eventos');
};
