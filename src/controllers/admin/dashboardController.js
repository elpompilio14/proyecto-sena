const pool = require('../../config/db');

exports.index = async (req, res) => {
    const mensajesNoLeidos = await pool.query(
        'SELECT COUNT(*) FROM mensajes_contacto WHERE leido = FALSE'
    );
    res.render('admin/dashboard', {
        titulo: 'Panel admin',
        mensajesNoLeidos: parseInt(mensajesNoLeidos.rows[0].count, 10),
    });
};
