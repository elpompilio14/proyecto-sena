const pool = require('../../config/db');

exports.index = async (req, res) => {
    const resultados = await pool.query('SELECT * FROM icfes_resultados ORDER BY anio DESC, puntaje DESC');
    res.render('admin/icfes', { titulo: 'Admin · Mejores ICFES', resultados: resultados.rows });
};

exports.crear = async (req, res) => {
    const { estudiante_nombre, puntaje, anio, descripcion } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        `INSERT INTO icfes_resultados (estudiante_nombre, puntaje, anio, foto_url, descripcion)
         VALUES ($1, $2, $3, $4, $5)`,
        [estudiante_nombre, puntaje, anio, foto_url, descripcion || null]
    );
    res.redirect('/admin/icfes');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM icfes_resultados WHERE id = $1', [req.params.id]);
    res.redirect('/admin/icfes');
};

exports.toggleVisible = async (req, res) => {
    const r = await pool.query('UPDATE icfes_resultados SET visible = NOT visible WHERE id = $1 RETURNING visible', [req.params.id]);
    res.json({ visible: r.rows[0].visible });
};

exports.editarForm = async (req, res) => {
    const resultado = await pool.query('SELECT * FROM icfes_resultados WHERE id = $1', [req.params.id]);
    if (resultado.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/icfes-editar', { titulo: 'Admin · Editar resultado ICFES', resultado: resultado.rows[0] });
};

exports.editar = async (req, res) => {
    const { estudiante_nombre, puntaje, anio, descripcion, foto_actual } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : (foto_actual || null);
    await pool.query(
        `UPDATE icfes_resultados SET estudiante_nombre = $1, puntaje = $2, anio = $3, foto_url = $4, descripcion = $5
         WHERE id = $6`,
        [estudiante_nombre, puntaje, anio, foto_url, descripcion || null, req.params.id]
    );
    res.redirect('/admin/icfes');
};
