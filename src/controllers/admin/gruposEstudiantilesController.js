const pool = require('../../config/db');

exports.index = async (req, res) => {
    const grupos = await pool.query('SELECT * FROM grupos_estudiantiles ORDER BY nombre');
    res.render('admin/grupos-estudiantiles', { titulo: 'Admin · Grupos Estudiantiles', grupos: grupos.rows });
};

exports.crear = async (req, res) => {
    const { nombre, descripcion, encargado } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        'INSERT INTO grupos_estudiantiles (nombre, descripcion, encargado, foto_url) VALUES ($1, $2, $3, $4)',
        [nombre, descripcion || null, encargado || null, foto_url]
    );
    res.redirect('/admin/grupos-estudiantiles');
};

exports.editarForm = async (req, res) => {
    const grupo = await pool.query('SELECT * FROM grupos_estudiantiles WHERE id = $1', [req.params.id]);
    if (grupo.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/grupos-estudiantiles-editar', { titulo: 'Admin · Editar grupo', grupo: grupo.rows[0] });
};

exports.editar = async (req, res) => {
    const { nombre, descripcion, encargado, foto_actual } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : (foto_actual || null);
    await pool.query(
        'UPDATE grupos_estudiantiles SET nombre = $1, descripcion = $2, encargado = $3, foto_url = $4 WHERE id = $5',
        [nombre, descripcion || null, encargado || null, foto_url, req.params.id]
    );
    res.redirect('/admin/grupos-estudiantiles');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM grupos_estudiantiles WHERE id = $1', [req.params.id]);
    res.redirect('/admin/grupos-estudiantiles');
};
