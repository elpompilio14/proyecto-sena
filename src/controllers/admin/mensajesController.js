const pool = require('../../config/db');

exports.index = async (req, res) => {
    const mensajes = await pool.query('SELECT * FROM mensajes_contacto ORDER BY creado_en DESC');
    res.render('admin/mensajes', { titulo: 'Admin · Mensajes', mensajes: mensajes.rows });
};

exports.marcarLeido = async (req, res) => {
    await pool.query('UPDATE mensajes_contacto SET leido = TRUE WHERE id = $1', [req.params.id]);
    res.redirect('/admin/mensajes');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM mensajes_contacto WHERE id = $1', [req.params.id]);
    res.redirect('/admin/mensajes');
};
