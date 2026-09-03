const pool = require('../../config/db');

exports.index = async (req, res) => {
    const info = await pool.query('SELECT * FROM institucion_info ORDER BY id LIMIT 1');
    res.render('admin/institucion', { titulo: 'Admin · Institución', info: info.rows[0] || null });
};

exports.actualizar = async (req, res) => {
    const {
        historia, mision, vision, principios, valores,
        ubicacion_sede1, ubicacion_sede2, telefono, correo,
        himno_url, himno_letra,
        escudo_texto, bandera_texto,
        escudo_url_actual, bandera_url_actual, fondo_url_actual, logo_url_actual,
        instagram_imagen_url_actual, facebook_imagen_url_actual, plataforma_virtual_logo_url_actual,
        manual_convivencia_url_actual, manual_convivencia_imagen_url_actual,
        promocion_logo_url_actual, promocion_link_url,
        anios_fundacion, num_estudiantes, num_profesores, whatsapp_numero,
        instagram_url, facebook_url, plataforma_virtual_url,
        articulado_texto, investigacion_texto,
    } = req.body;

    const archivoEscudo = req.files && req.files.escudo ? req.files.escudo[0] : null;
    const archivoBandera = req.files && req.files.bandera ? req.files.bandera[0] : null;
    const archivoFondo = req.files && req.files.fondo ? req.files.fondo[0] : null;
    const archivoLogo = req.files && req.files.logo ? req.files.logo[0] : null;
    const archivoInstagram = req.files && req.files.instagram_imagen ? req.files.instagram_imagen[0] : null;
    const archivoFacebook = req.files && req.files.facebook_imagen ? req.files.facebook_imagen[0] : null;
    const archivoPlataforma = req.files && req.files.plataforma_virtual_logo ? req.files.plataforma_virtual_logo[0] : null;
    const archivoManual = req.files && req.files.manual_convivencia ? req.files.manual_convivencia[0] : null;
    const archivoManualImagen = req.files && req.files.manual_convivencia_imagen ? req.files.manual_convivencia_imagen[0] : null;
    const archivoPromocion = req.files && req.files.promocion_logo ? req.files.promocion_logo[0] : null;

    const escudo_url = archivoEscudo ? `/images/${archivoEscudo.filename}` : (escudo_url_actual || null);
    const bandera_url = archivoBandera ? `/images/${archivoBandera.filename}` : (bandera_url_actual || null);
    const fondo_url = archivoFondo ? `/images/${archivoFondo.filename}` : (fondo_url_actual || null);
    const logo_url = archivoLogo ? `/images/${archivoLogo.filename}` : (logo_url_actual || null);
    const instagram_imagen_url = archivoInstagram ? `/images/${archivoInstagram.filename}` : (instagram_imagen_url_actual || null);
    const facebook_imagen_url = archivoFacebook ? `/images/${archivoFacebook.filename}` : (facebook_imagen_url_actual || null);
    const plataforma_virtual_logo_url = archivoPlataforma ? `/images/${archivoPlataforma.filename}` : (plataforma_virtual_logo_url_actual || null);
    const manual_convivencia_url = archivoManual ? `/images/${archivoManual.filename}` : (manual_convivencia_url_actual || null);
    const manual_convivencia_imagen_url = archivoManualImagen ? `/images/${archivoManualImagen.filename}` : (manual_convivencia_imagen_url_actual || null);
    const promocion_logo_url = archivoPromocion ? `/images/${archivoPromocion.filename}` : (promocion_logo_url_actual || null);

    const existente = await pool.query('SELECT id FROM institucion_info ORDER BY id LIMIT 1');

    const valores_comunes = [
        historia, mision, vision, principios, valores, ubicacion_sede1, ubicacion_sede2,
        telefono || null, correo || null, himno_url || null, himno_letra || null,
        escudo_texto || null, escudo_url, bandera_texto || null, bandera_url, fondo_url,
        logo_url, anios_fundacion || null, num_estudiantes || null, num_profesores || null,
        whatsapp_numero || null, instagram_url || null, instagram_imagen_url,
        facebook_url || null, facebook_imagen_url,
        plataforma_virtual_url || null, plataforma_virtual_logo_url,
        manual_convivencia_url, manual_convivencia_imagen_url,
        articulado_texto || null, investigacion_texto || null,
        promocion_logo_url, promocion_link_url || null,
    ];

    if (existente.rows.length === 0) {
        await pool.query(
            `INSERT INTO institucion_info
                (historia, mision, vision, principios, valores, ubicacion_sede1, ubicacion_sede2,
                 telefono, correo, himno_url, himno_letra, escudo_texto, escudo_url, bandera_texto, bandera_url, fondo_url,
                 logo_url, anios_fundacion, num_estudiantes, num_profesores, whatsapp_numero,
                 instagram_url, instagram_imagen_url, facebook_url, facebook_imagen_url,
                 plataforma_virtual_url, plataforma_virtual_logo_url,
                 manual_convivencia_url, manual_convivencia_imagen_url,
                 articulado_texto, investigacion_texto,
                 promocion_logo_url, promocion_link_url)
             VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16,
                     $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32, $33)`,
            valores_comunes
        );
    } else {
        await pool.query(
            `UPDATE institucion_info
             SET historia = $1, mision = $2, vision = $3, principios = $4, valores = $5,
                 ubicacion_sede1 = $6, ubicacion_sede2 = $7, telefono = $8, correo = $9,
                 himno_url = $10, himno_letra = $11,
                 escudo_texto = $12, escudo_url = $13, bandera_texto = $14, bandera_url = $15,
                 fondo_url = $16, logo_url = $17, anios_fundacion = $18, num_estudiantes = $19,
                 num_profesores = $20, whatsapp_numero = $21, instagram_url = $22,
                 instagram_imagen_url = $23, facebook_url = $24, facebook_imagen_url = $25,
                 plataforma_virtual_url = $26, plataforma_virtual_logo_url = $27,
                 manual_convivencia_url = $28, manual_convivencia_imagen_url = $29,
                 articulado_texto = $30, investigacion_texto = $31,
                 promocion_logo_url = $32, promocion_link_url = $33,
                 actualizado_en = NOW()
             WHERE id = $34`,
            [...valores_comunes, existente.rows[0].id]
        );
    }

    res.redirect('/admin/institucion');
};
