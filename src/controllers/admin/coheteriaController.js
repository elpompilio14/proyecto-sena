const pool = require('../../config/db');

exports.index = async (req, res) => {
    const miembros = await pool.query('SELECT * FROM coheteria ORDER BY orden, nombre');
    const info = await pool.query('SELECT coheteria_texto, coheteria_portada_url FROM institucion_info ORDER BY id LIMIT 1');
    res.render('admin/coheteria', {
        titulo: 'Admin · Cohetería',
        miembros: miembros.rows,
        infoTexto: info.rows[0] ? info.rows[0].coheteria_texto : '',
        infoPortada: info.rows[0] ? info.rows[0].coheteria_portada_url : null,
    });
};

exports.actualizarInfo = async (req, res) => {
    const { texto, portada_actual } = req.body;
    const portada_url = req.file ? `/images/${req.file.filename}` : (portada_actual || null);
    await pool.query(
        'UPDATE institucion_info SET coheteria_texto = $1, coheteria_portada_url = $2 WHERE id = (SELECT id FROM institucion_info ORDER BY id LIMIT 1)',
        [texto || null, portada_url]
    );
    res.redirect('/admin/coheteria');
};

exports.crear = async (req, res) => {
    const { nombre, rol, salon, orden, nivel } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        'INSERT INTO coheteria (nombre, rol, salon, foto_url, orden, nivel) VALUES ($1, $2, $3, $4, $5, $6)',
        [nombre, rol || null, salon || null, foto_url, orden || 0, nivel || 'base']
    );
    res.redirect('/admin/coheteria');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM coheteria WHERE id = $1', [req.params.id]);
    res.redirect('/admin/coheteria');
};

exports.toggleVisible = async (req, res) => {
    const r = await pool.query('UPDATE coheteria SET visible = NOT visible WHERE id = $1 RETURNING visible', [req.params.id]);
    res.json({ visible: r.rows[0].visible });
};

exports.editarForm = async (req, res) => {
    const miembro = await pool.query('SELECT * FROM coheteria WHERE id = $1', [req.params.id]);
    if (miembro.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/coheteria-editar', { titulo: 'Admin · Editar miembro', miembro: miembro.rows[0] });
};

exports.editar = async (req, res) => {
    const { nombre, rol, salon, foto_actual, orden, nivel } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : (foto_actual || null);
    await pool.query(
        'UPDATE coheteria SET nombre = $1, rol = $2, salon = $3, foto_url = $4, orden = $5, nivel = $6 WHERE id = $7',
        [nombre, rol || null, salon || null, foto_url, orden || 0, nivel || 'base', req.params.id]
    );
    res.redirect('/admin/coheteria');
};
