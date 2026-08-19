const bcrypt = require('bcryptjs');
const pool = require('../config/db');

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
    const resultado = await pool.query(
        `INSERT INTO usuarios (nombre, apellido, email, password_hash, rol)
         VALUES ($1, $2, $3, $4, 'usuario')
         RETURNING id, nombre, rol`,
        [nombre, apellido, email, password_hash]
    );

    req.session.usuario = resultado.rows[0];
    res.redirect('/');
};

exports.loginForm = (req, res) => {
    res.render('auth', { titulo: 'Iniciar sesión', tabActiva: 'login', errorLogin: null, errorRegistro: null });
};

exports.login = async (req, res) => {
    const { email, password } = req.body;
    const resultado = await pool.query('SELECT * FROM usuarios WHERE email = $1', [email]);
    const usuario = resultado.rows[0];

    if (!usuario || !(await bcrypt.compare(password, usuario.password_hash))) {
        return res.status(401).render('auth', {
            titulo: 'Iniciar sesión',
            tabActiva: 'login',
            errorLogin: 'Correo o contraseña incorrectos',
            errorRegistro: null,
        });
    }

    req.session.usuario = { id: usuario.id, nombre: usuario.nombre, rol: usuario.rol };
    res.redirect(usuario.rol === 'admin' ? '/admin' : '/');
};

exports.logout = (req, res) => {
    req.session.destroy(() => res.redirect('/login'));
};
