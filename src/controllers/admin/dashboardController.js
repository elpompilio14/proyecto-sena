const pool = require('../../config/db');

exports.index = async (req, res) => {
    const mensajesNoLeidos = await pool.query(
        'SELECT COUNT(*) FROM mensajes_contacto WHERE leido = FALSE'
    );
    const mediaTecnicaCategorias = await pool.query(
        'SELECT id, nombre FROM media_tecnica_categorias ORDER BY orden, nombre'
    );
    res.render('admin/dashboard', {
        titulo: 'Panel admin',
        mensajesNoLeidos: parseInt(mensajesNoLeidos.rows[0].count, 10),
        mediaTecnicaCategorias: mediaTecnicaCategorias.rows,
    });
};
