const pool = require('../../config/db');

exports.index = async (req, res) => {
    const resultados = await pool.query(`
        SELECT resultados.*, c.nombre AS campeonato_nombre,
               el.nombre AS equipo_local_nombre, ev.nombre AS equipo_visitante_nombre
        FROM resultados
        JOIN campeonatos c ON c.id = resultados.campeonato_id
        JOIN equipos el ON el.id = resultados.equipo_local_id
        JOIN equipos ev ON ev.id = resultados.equipo_visitante_id
        ORDER BY resultados.fecha DESC
    `);
    const campeonatos = await pool.query('SELECT id, nombre FROM campeonatos ORDER BY nombre');
    const equipos = await pool.query('SELECT id, nombre FROM equipos ORDER BY nombre');
    res.render('admin/resultados', {
        titulo: 'Admin · Resultados',
        resultados: resultados.rows,
        campeonatos: campeonatos.rows,
        equipos: equipos.rows,
    });
};

exports.crear = async (req, res) => {
    const { campeonato_id, equipo_local_id, equipo_visitante_id, marcador_local, marcador_visitante, fecha } = req.body;
    await pool.query(
        `INSERT INTO resultados (campeonato_id, equipo_local_id, equipo_visitante_id, marcador_local, marcador_visitante, fecha)
         VALUES ($1, $2, $3, $4, $5, $6)`,
        [campeonato_id, equipo_local_id, equipo_visitante_id, marcador_local || 0, marcador_visitante || 0, fecha]
    );
    res.redirect('/admin/resultados');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM resultados WHERE id = $1', [req.params.id]);
    res.redirect('/admin/resultados');
};

exports.editarForm = async (req, res) => {
    const resultado = await pool.query('SELECT * FROM resultados WHERE id = $1', [req.params.id]);
    if (resultado.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    const campeonatos = await pool.query('SELECT id, nombre FROM campeonatos ORDER BY nombre');
    const equipos = await pool.query('SELECT id, nombre FROM equipos ORDER BY nombre');
    res.render('admin/resultados-editar', {
        titulo: 'Admin · Editar resultado',
        resultado: resultado.rows[0],
        campeonatos: campeonatos.rows,
        equipos: equipos.rows,
    });
};

exports.editar = async (req, res) => {
    const { campeonato_id, equipo_local_id, equipo_visitante_id, marcador_local, marcador_visitante, fecha } = req.body;
    await pool.query(
        `UPDATE resultados SET campeonato_id = $1, equipo_local_id = $2, equipo_visitante_id = $3,
         marcador_local = $4, marcador_visitante = $5, fecha = $6
         WHERE id = $7`,
        [campeonato_id, equipo_local_id, equipo_visitante_id, marcador_local || 0, marcador_visitante || 0, fecha, req.params.id]
    );
    res.redirect('/admin/resultados');
};
