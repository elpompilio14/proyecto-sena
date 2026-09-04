require('dotenv').config();
const path = require('path');
const fs = require('fs');
const express = require('express');
const session = require('express-session');

const publicRoutes = require('./routes/public');
const authRoutes = require('./routes/auth');
const adminRoutes = require('./routes/admin');
const formatearTexto = require('./utils/formatearTexto');
const esVideo = require('./utils/esVideo');
const youtubeEmbedUrl = require('./utils/youtubeEmbedUrl');
const googleMapsEmbedUrl = require('./utils/googleMapsEmbedUrl');
const whatsappNumero = require('./utils/whatsappNumero');
const pool = require('./config/db');

const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.locals.formatearTexto = formatearTexto;
app.locals.esVideo = esVideo;
app.locals.youtubeEmbedUrl = youtubeEmbedUrl;
app.locals.googleMapsEmbedUrl = googleMapsEmbedUrl;
app.locals.whatsappNumero = whatsappNumero;

app.use(express.static(path.join(__dirname, '..', 'public')));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(session({
    secret: process.env.SESSION_SECRET || 'dev-secret',
    resave: false,
    saveUninitialized: false,
    cookie: { maxAge: 1000 * 60 * 60 * 4 }, // 4 horas
}));

const rutaCss = path.join(__dirname, '..', 'public', 'css', 'style.css');
const rutaHeroJs = path.join(__dirname, '..', 'public', 'js', 'hero-carrusel.js');
const rutaVolverArribaJs = path.join(__dirname, '..', 'public', 'js', 'volver-arriba.js');

app.use((req, res, next) => {
    res.locals.usuario = req.session.usuario || null;
    res.locals.esAdmin = req.path.startsWith('/admin');
    try {
        res.locals.cssVersion = fs.statSync(rutaCss).mtimeMs;
    } catch (err) {
        res.locals.cssVersion = Date.now();
    }
    try {
        res.locals.heroJsVersion = fs.statSync(rutaHeroJs).mtimeMs;
    } catch (err) {
        res.locals.heroJsVersion = Date.now();
    }
    try {
        res.locals.volverArribaJsVersion = fs.statSync(rutaVolverArribaJs).mtimeMs;
    } catch (err) {
        res.locals.volverArribaJsVersion = Date.now();
    }
    next();
});

app.use(async (req, res, next) => {
    try {
        const { rows } = await pool.query('SELECT * FROM institucion_info ORDER BY id LIMIT 1');
        res.locals.contacto = rows[0] || {};
        res.locals.sitio = rows[0] || {};
    } catch (err) {
        res.locals.contacto = {};
        res.locals.sitio = {};
    }
    next();
});

app.use('/', publicRoutes);
app.use('/', authRoutes);
app.use('/admin', adminRoutes);

app.use((req, res) => {
    res.status(404).render('404', { titulo: 'Pagina no encontrada' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
