require('dotenv').config();
const path = require('path');
const express = require('express');
const session = require('express-session');

const publicRoutes = require('./routes/public');
const authRoutes = require('./routes/auth');
const adminRoutes = require('./routes/admin');
const formatearTexto = require('./utils/formatearTexto');
const esVideo = require('./utils/esVideo');
const youtubeEmbedUrl = require('./utils/youtubeEmbedUrl');
const googleMapsEmbedUrl = require('./utils/googleMapsEmbedUrl');

const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.locals.formatearTexto = formatearTexto;
app.locals.esVideo = esVideo;
app.locals.youtubeEmbedUrl = youtubeEmbedUrl;
app.locals.googleMapsEmbedUrl = googleMapsEmbedUrl;

app.use(express.static(path.join(__dirname, '..', 'public')));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(session({
    secret: process.env.SESSION_SECRET || 'dev-secret',
    resave: false,
    saveUninitialized: false,
    cookie: { maxAge: 1000 * 60 * 60 * 4 }, // 4 horas
}));

app.use((req, res, next) => {
    res.locals.usuario = req.session.usuario || null;
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
