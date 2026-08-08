const path = require('path');
const multer = require('multer');

const storage = multer.diskStorage({
    destination: path.join(__dirname, '..', '..', 'public', 'images'),
    filename: (req, file, cb) => {
        const extension = path.extname(file.originalname).toLowerCase();
        const nombreUnico = `${Date.now()}-${Math.round(Math.random() * 1e9)}${extension}`;
        cb(null, nombreUnico);
    },
});

const tiposImagen = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
const tiposImagenYVideo = [...tiposImagen, '.mp4', '.webm', '.mov', '.ogg'];

function crearFiltro(tiposPermitidos, mensajeError) {
    return function filtroArchivo(req, file, cb) {
        const extension = path.extname(file.originalname).toLowerCase();
        if (!tiposPermitidos.includes(extension)) {
            return cb(new Error(mensajeError));
        }
        cb(null, true);
    };
}

// Para fotos de portada (eventos, noticias, equipos, estudiantes): solo imagenes
const upload = multer({
    storage,
    fileFilter: crearFiltro(tiposImagen, 'Solo se permiten imágenes (jpg, png, gif, webp)'),
    limits: { fileSize: 5 * 1024 * 1024 },
});

// Para la galeria: imagenes y videos cortos
const uploadGaleria = multer({
    storage,
    fileFilter: crearFiltro(tiposImagenYVideo, 'Solo se permiten imágenes (jpg, png, gif, webp) o videos (mp4, webm, mov, ogg)'),
    limits: { fileSize: 50 * 1024 * 1024 },
});

module.exports = upload;
module.exports.galeria = uploadGaleria;
