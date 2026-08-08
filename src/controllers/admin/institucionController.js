const pool = require('../../config/db');

exports.index = async (req, res) => {
    const info = await pool.query('SELECT * FROM institucion_info ORDER BY id LIMIT 1');
    res.render('admin/institucion', { titulo: 'Admin · Institución', info: info.rows[0] || null });
};

exports.actualizar = async (req, res) => {
    const {
        historia, mision, vision, principios, valores, ubicacion,
        himno_url, himno_letra,
        escudo_texto, bandera_texto,
        escudo_url_actual, bandera_url_actual,
    } = req.body;

    const archivoEscudo = req.files && req.files.escudo ? req.files.escudo[0] : null;
    const archivoBandera = req.files && req.files.bandera ? req.files.bandera[0] : null;

    const escudo_url = archivoEscudo ? `/images/${archivoEscudo.filename}` : (escudo_url_actual || null);
    const bandera_url = archivoBandera ? `/images/${archivoBandera.filename}` : (bandera_url_actual || null);

    const existente = await pool.query('SELECT id FROM institucion_info ORDER BY id LIMIT 1');

    if (existente.rows.length === 0) {
        await pool.query(
            `INSERT INTO institucion_info
                (historia, mision, vision, principios, valores, ubicacion, himno_url, himno_letra,
                 escudo_texto, escudo_url, bandera_texto, bandera_url)
             VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)`,
            [historia, mision, vision, principios, valores, ubicacion, himno_url || null, himno_letra || null,
                escudo_texto || null, escudo_url, bandera_texto || null, bandera_url]
        );
    } else {
        await pool.query(
            `UPDATE institucion_info
             SET historia = $1, mision = $2, vision = $3, principios = $4, valores = $5, ubicacion = $6,
                 himno_url = $7, himno_letra = $8,
                 escudo_texto = $9, escudo_url = $10, bandera_texto = $11, bandera_url = $12,
                 actualizado_en = NOW()
             WHERE id = $13`,
            [historia, mision, vision, principios, valores, ubicacion, himno_url || null, himno_letra || null,
                escudo_texto || null, escudo_url, bandera_texto || null, bandera_url, existente.rows[0].id]
        );
    }

    res.redirect('/admin/institucion');
};
