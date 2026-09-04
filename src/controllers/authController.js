const crypto = require('crypto');
const bcrypt = require('bcryptjs');
const pool = require('../config/db');
const generarCodigo = require('../utils/generarCodigo');
const { enviarCodigoVerificacion, enviarCodigoRecuperacion } = require('../config/mailer');
const { urlAutorizacionGoogle, obtenerPerfilGoogle } = require('../utils/googleAuth');

const MINUTOS_EXPIRACION_CODIGO = 15;

exports.registroForm = (req, res) => {
    res.render('auth', { titulo: 'Crear cuenta', tabActiva: 'registro', errorLogin: null, errorRegistro: null });
};

exports.registro = async (req, res) => {
    const { nombre, apellido, email, password, password_confirmar } = req.body;

    if (!nombre || !apellido || !email || !password || !password_confirmar) {
        return res.status(400).render('auth', {
            titulo: 'Crear cuenta',
            tabActiva: 'registro',
            errorLogin: null,
            errorRegistro: 'Todos los campos son obligatorios',
        });
    }

    if (password !== password_confirmar) {
        return res.status(400).render('auth', {
            titulo: 'Crear cuenta',
            tabActiva: 'registro',
            errorLogin: null,
            errorRegistro: 'Las contraseñas no coinciden',
        });
    }

    const existente = await pool.query('SELECT id FROM usuarios WHERE email = $1', [email]);
    if (existente.rows.length > 0) {
        return res.status(400).render('auth', {
            titulo: 'Crear cuenta',
            tabActiva: 'registro',
            errorLogin: null,
            errorRegistro: 'Ese correo ya está registrado',
        });
    }

    const password_hash = await bcrypt.hash(password, 10);
    const codigo = generarCodigo();
    const expira = new Date(Date.now() + MINUTOS_EXPIRACION_CODIGO * 60 * 1000);

    await pool.query(
        `INSERT INTO usuarios (nombre, apellido, email, password_hash, rol, verificado, codigo_verificacion, codigo_expira)
         VALUES ($1, $2, $3, $4, 'usuario', false, $5, $6)`,
        [nombre, apellido, email, password_hash, codigo, expira]
    );

    try {
        await enviarCodigoVerificacion(email, nombre, codigo);
    } catch (err) {
        console.error('No se pudo enviar el correo de verificación:', err.message);
    }

    res.redirect(`/verificar-correo?email=${encodeURIComponent(email)}`);
};

exports.verificarForm = (req, res) => {
    res.render('verificar-correo', { titulo: 'Verificar correo', email: req.query.email || '', error: null });
};

exports.verificar = async (req, res) => {
    const { email, codigo } = req.body;

    const resultado = await pool.query('SELECT * FROM usuarios WHERE email = $1', [email]);
    const usuario = resultado.rows[0];

    if (!usuario) {
        return res.status(400).render('verificar-correo', { titulo: 'Verificar correo', email, error: 'No encontramos esa cuenta' });
    }

    if (usuario.verificado) {
        req.session.usuario = { id: usuario.id, nombre: usuario.nombre, rol: usuario.rol };
        return res.redirect('/');
    }

    const expirado = !usuario.codigo_expira || new Date(usuario.codigo_expira) < new Date();
    if (expirado) {
        return res.status(400).render('verificar-correo', {
            titulo: 'Verificar correo', email, error: 'El código venció, pide uno nuevo',
        });
    }

    if (usuario.codigo_verificacion !== codigo) {
        return res.status(400).render('verificar-correo', { titulo: 'Verificar correo', email, error: 'Código incorrecto' });
    }

    await pool.query(
        'UPDATE usuarios SET verificado = true, codigo_verificacion = null, codigo_expira = null WHERE id = $1',
        [usuario.id]
    );

    req.session.usuario = { id: usuario.id, nombre: usuario.nombre, rol: usuario.rol };
    res.redirect('/');
};

exports.reenviarCodigo = async (req, res) => {
    const { email } = req.body;
    const resultado = await pool.query('SELECT * FROM usuarios WHERE email = $1', [email]);
    const usuario = resultado.rows[0];

    if (usuario && !usuario.verificado) {
        const codigo = generarCodigo();
        const expira = new Date(Date.now() + MINUTOS_EXPIRACION_CODIGO * 60 * 1000);
        await pool.query('UPDATE usuarios SET codigo_verificacion = $1, codigo_expira = $2 WHERE id = $3', [codigo, expira, usuario.id]);
        try {
            await enviarCodigoVerificacion(usuario.email, usuario.nombre, codigo);
        } catch (err) {
            console.error('No se pudo reenviar el correo de verificación:', err.message);
        }
    }

    res.render('verificar-correo', { titulo: 'Verificar correo', email, error: null, reenviado: true });
};

exports.loginForm = (req, res) => {
    res.render('auth', {
        titulo: 'Iniciar sesión',
        tabActiva: 'login',
        errorLogin: null,
        errorRegistro: null,
        exitoLogin: req.query.restablecida ? 'Tu contraseña fue actualizada. Ya puedes iniciar sesión.' : null,
    });
};

exports.login = async (req, res) => {
    const { email, password } = req.body;
    const resultado = await pool.query('SELECT * FROM usuarios WHERE email = $1', [email]);
    const usuario = resultado.rows[0];

    if (!usuario || !usuario.password_hash) {
        return res.status(401).render('auth', {
            titulo: 'Iniciar sesión',
            tabActiva: 'login',
            errorLogin: !usuario ? 'Correo o contraseña incorrectos' : 'Esta cuenta inicia sesión con Google, usa ese botón',
            errorRegistro: null,
        });
    }

    if (!(await bcrypt.compare(password, usuario.password_hash))) {
        return res.status(401).render('auth', {
            titulo: 'Iniciar sesión',
            tabActiva: 'login',
            errorLogin: 'Correo o contraseña incorrectos',
            errorRegistro: null,
        });
    }

    if (!usuario.verificado) {
        return res.redirect(`/verificar-correo?email=${encodeURIComponent(usuario.email)}`);
    }

    req.session.usuario = { id: usuario.id, nombre: usuario.nombre, rol: usuario.rol };
    res.redirect(usuario.rol === 'admin' ? '/admin' : '/');
};

exports.logout = (req, res) => {
    req.session.destroy(() => res.redirect('/login'));
};

exports.recuperarForm = (req, res) => {
    res.render('recuperar-contrasena', { titulo: 'Recuperar contraseña', error: null });
};

exports.recuperar = async (req, res) => {
    const { email } = req.body;
    const resultado = await pool.query('SELECT * FROM usuarios WHERE email = $1', [email]);
    const usuario = resultado.rows[0];

    if (!usuario) {
        return res.status(400).render('recuperar-contrasena', {
            titulo: 'Recuperar contraseña',
            error: 'No encontramos una cuenta con ese correo',
        });
    }

    if (!usuario.password_hash) {
        return res.status(400).render('recuperar-contrasena', {
            titulo: 'Recuperar contraseña',
            error: 'Esta cuenta inicia sesión con Google, no tiene contraseña que restablecer',
        });
    }

    const codigo = generarCodigo();
    const expira = new Date(Date.now() + MINUTOS_EXPIRACION_CODIGO * 60 * 1000);
    await pool.query('UPDATE usuarios SET codigo_verificacion = $1, codigo_expira = $2 WHERE id = $3', [codigo, expira, usuario.id]);

    try {
        await enviarCodigoRecuperacion(usuario.email, usuario.nombre, codigo);
    } catch (err) {
        console.error('No se pudo enviar el correo de recuperación:', err.message);
    }

    res.redirect(`/recuperar-contrasena/verificar?email=${encodeURIComponent(email)}`);
};

exports.recuperarVerificarForm = (req, res) => {
    res.render('recuperar-contrasena-verificar', {
        titulo: 'Restablecer contraseña',
        email: req.query.email || '',
        error: null,
    });
};

exports.recuperarVerificar = async (req, res) => {
    const { email, codigo, password, password_confirmar } = req.body;

    const resultado = await pool.query('SELECT * FROM usuarios WHERE email = $1', [email]);
    const usuario = resultado.rows[0];

    if (!usuario) {
        return res.status(400).render('recuperar-contrasena-verificar', {
            titulo: 'Restablecer contraseña', email, error: 'No encontramos esa cuenta',
        });
    }

    const expirado = !usuario.codigo_expira || new Date(usuario.codigo_expira) < new Date();
    if (expirado) {
        return res.status(400).render('recuperar-contrasena-verificar', {
            titulo: 'Restablecer contraseña', email, error: 'El código venció, pide uno nuevo',
        });
    }

    if (usuario.codigo_verificacion !== codigo) {
        return res.status(400).render('recuperar-contrasena-verificar', {
            titulo: 'Restablecer contraseña', email, error: 'Código incorrecto',
        });
    }

    if (!password || password.length < 6) {
        return res.status(400).render('recuperar-contrasena-verificar', {
            titulo: 'Restablecer contraseña', email, error: 'La contraseña debe tener al menos 6 caracteres',
        });
    }

    if (password !== password_confirmar) {
        return res.status(400).render('recuperar-contrasena-verificar', {
            titulo: 'Restablecer contraseña', email, error: 'Las contraseñas no coinciden',
        });
    }

    const password_hash = await bcrypt.hash(password, 10);
    await pool.query(
        'UPDATE usuarios SET password_hash = $1, verificado = true, codigo_verificacion = null, codigo_expira = null WHERE id = $2',
        [password_hash, usuario.id]
    );

    res.redirect('/login?restablecida=1');
};

exports.iniciarGoogle = (req, res) => {
    const state = crypto.randomBytes(16).toString('hex');
    req.session.googleState = state;
    res.redirect(urlAutorizacionGoogle(state));
};

exports.callbackGoogle = async (req, res) => {
    const { code, state } = req.query;

    if (!code || !state || state !== req.session.googleState) {
        return res.redirect('/login');
    }

    try {
        const perfil = await obtenerPerfilGoogle(code);

        let resultado = await pool.query('SELECT * FROM usuarios WHERE google_id = $1', [perfil.id]);
        let usuario = resultado.rows[0];

        if (!usuario) {
            resultado = await pool.query('SELECT * FROM usuarios WHERE email = $1', [perfil.email]);
            usuario = resultado.rows[0];

            if (usuario) {
                await pool.query('UPDATE usuarios SET google_id = $1, verificado = true WHERE id = $2', [perfil.id, usuario.id]);
            } else {
                const nuevo = await pool.query(
                    `INSERT INTO usuarios (nombre, apellido, email, password_hash, rol, verificado, google_id)
                     VALUES ($1, $2, $3, NULL, 'usuario', true, $4)
                     RETURNING id, nombre, rol`,
                    [perfil.given_name || perfil.name || 'Usuario', perfil.family_name || '', perfil.email, perfil.id]
                );
                usuario = nuevo.rows[0];
            }
        }

        req.session.usuario = { id: usuario.id, nombre: usuario.nombre, rol: usuario.rol };
        res.redirect(usuario.rol === 'admin' ? '/admin' : '/');
    } catch (err) {
        console.error('Error en login con Google:', err.message);
        res.redirect('/login');
    }
};
