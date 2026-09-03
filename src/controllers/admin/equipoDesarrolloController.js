const pool = require('../../config/db');

exports.index = async (req, res) => {
    const miembros = await pool.query('SELECT * FROM equipo_desarrollo ORDER BY orden, nombre');
    const info = await pool.query('SELECT equipo_desarrollo_texto, equipo_desarrollo_portada_url FROM institucion_info ORDER BY id LIMIT 1');
    res.render('admin/equipo-desarrollo', {
        titulo: 'Admin · Equipo de Desarrollo',
        miembros: miembros.rows,
        infoTexto: info.rows[0] ? info.rows[0].equipo_desarrollo_texto : '',
        infoPortada: info.rows[0] ? info.rows[0].equipo_desarrollo_portada_url : null,
    });
};

exports.actualizarInfo = async (req, res) => {
    const { texto, portada_actual } = req.body;
    const portada_url = req.file ? `/images/${req.file.filename}` : (portada_actual || null);
    await pool.query(
        'UPDATE institucion_info SET equipo_desarrollo_texto = $1, equipo_desarrollo_portada_url = $2 WHERE id = (SELECT id FROM institucion_info ORDER BY id LIMIT 1)',
        [texto || null, portada_url]
    );
    res.redirect('/admin/equipo-desarrollo');
};

exports.crear = async (req, res) => {
    const { nombre, rol, orden, nivel } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : null;
    await pool.query(
        'INSERT INTO equipo_desarrollo (nombre, rol, foto_url, orden, nivel) VALUES ($1, $2, $3, $4, $5)',
        [nombre, rol || null, foto_url, orden || 0, nivel || 'base']
    );
    res.redirect('/admin/equipo-desarrollo');
};

exports.eliminar = async (req, res) => {
    await pool.query('DELETE FROM equipo_desarrollo WHERE id = $1', [req.params.id]);
    res.redirect('/admin/equipo-desarrollo');
};

exports.toggleVisible = async (req, res) => {
    const r = await pool.query('UPDATE equipo_desarrollo SET visible = NOT visible WHERE id = $1 RETURNING visible', [req.params.id]);
    res.json({ visible: r.rows[0].visible });
};

exports.editarForm = async (req, res) => {
    const miembro = await pool.query('SELECT * FROM equipo_desarrollo WHERE id = $1', [req.params.id]);
    if (miembro.rows.length === 0) {
        return res.status(404).render('404', { titulo: 'No encontrado' });
    }
    res.render('admin/equipo-desarrollo-editar', { titulo: 'Admin · Editar miembro', miembro: miembro.rows[0] });
};

exports.editar = async (req, res) => {
    const { nombre, rol, foto_actual, orden, nivel } = req.body;
    const foto_url = req.file ? `/images/${req.file.filename}` : (foto_actual || null);
    await pool.query(
        'UPDATE equipo_desarrollo SET nombre = $1, rol = $2, foto_url = $3, orden = $4, nivel = $5 WHERE id = $6',
        [nombre, rol || null, foto_url, orden || 0, nivel || 'base', req.params.id]
    );
    res.redirect('/admin/equipo-desarrollo');
};
