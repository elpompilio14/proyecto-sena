const pool = require('../../config/db');

exports.index = async (req, res) => {
    const puestos = await pool.query(`
        SELECT mejores_puestos.*, estudiantes.nombres, estudiantes.apellidos, grados.nombre AS grado_nombre
        FROM mejores_puestos
        JOIN estudiantes ON estudiantes.id = mejores_puestos.estudiante_id
        JOIN grados ON grados.id = mejores_puestos.grado_id
        ORDER BY grados.nivel, mejores_puestos.periodo DESC, mejores_puestos.puesto
    `);
    const estudiantes = await pool.query('SELECT id, nombres, apellidos FROM estudiantes ORDER BY apellidos, nombres');
    const grados = await pool.query('SELECT * FROM grados ORDER BY nivel, nombre');
    res.render('admin/mejores-puestos', {
        titulo: 'Admin · Puestos de honor',
        puestos: puestos.rows,
        estudiantes: estudiantes.rows,
        grados: grados.rows,
    });
};

exports.crear = async (req, res) => {
    const { estudiante_id, grado_id, periodo, puesto, promedio } = req.body;
    await pool.query(
        `INSERT INTO mejores_puestos (estudiante_id, grado_id, periodo, puesto, promedio)
         VALUES ($1, $2, $3, $4, $5)`,
        [estudiante_id, grado_id, periodo, puesto, promedio || null]
    );
    res.redirect('/admin/mejores-puestos');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM mejores_puestos WHERE id = $1', [req.params.id]);
    res.redirect('/admin/mejores-puestos');
};

exports.editarForm = async (req, res) => {
    const puesto = await pool.query('SELECT * FROM mejores_puestos WHERE id = $1', [req.params.id]);
    if (puesto.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    const estudiantes = await pool.query('SELECT id, nombres, apellidos FROM estudiantes ORDER BY apellidos, nombres');
    const grados = await pool.query('SELECT * FROM grados ORDER BY nivel, nombre');
    res.render('admin/mejores-puestos-editar', {
        titulo: 'Admin · Editar puesto de honor',
        puesto: puesto.rows[0],
        estudiantes: estudiantes.rows,
        grados: grados.rows,
    });
};

exports.editar = async (req, res) => {
    const { estudiante_id, grado_id, periodo, puesto, promedio } = req.body;
    await pool.query(
        `UPDATE mejores_puestos SET estudiante_id = $1, grado_id = $2, periodo = $3, puesto = $4, promedio = $5
         WHERE id = $6`,
        [estudiante_id, grado_id, periodo, puesto, promedio || null, req.params.id]
    );
    res.redirect('/admin/mejores-puestos');
};
