const express = require('express');
const router = express.Router();
const requireAdmin = require('../middlewares/requireAdmin');
const upload = require('../config/upload');

const dashboardController = require('../controllers/admin/dashboardController');
const eventosController = require('../controllers/admin/eventosController');
const noticiasController = require('../controllers/admin/noticiasController');
const fotosController = require('../controllers/admin/fotosController');
const equiposController = require('../controllers/admin/equiposController');
const campeonatosController = require('../controllers/admin/campeonatosController');
const resultadosController = require('../controllers/admin/resultadosController');
const estudiantesController = require('../controllers/admin/estudiantesController');
const mejoresPuestosController = require('../controllers/admin/mejoresPuestosController');
const institucionController = require('../controllers/admin/institucionController');
const mensajesController = require('../controllers/admin/mensajesController');
const gradosController = require('../controllers/admin/gradosController');
const deportesController = require('../controllers/admin/deportesController');
const mediaTecnicaController = require('../controllers/admin/mediaTecnicaController');
const gruposEstudiantilesController = require('../controllers/admin/gruposEstudiantilesController');
const comunidadController = require('../controllers/admin/comunidadController');
const icfesController = require('../controllers/admin/icfesController');
const alianzasController = require('../controllers/admin/alianzasController');
const gobiernoEscolarController = require('../controllers/admin/gobiernoEscolarController');
const equipoDesarrolloController = require('../controllers/admin/equipoDesarrolloController');
const comiteEcologicoController = require('../controllers/admin/comiteEcologicoController');
const equipoDronesController = require('../controllers/admin/equipoDronesController');
const coheteriaController = require('../controllers/admin/coheteriaController');

router.use(requireAdmin);

router.get('/', dashboardController.index);

router.get('/eventos', eventosController.index);
router.post('/eventos', upload.single('imagen'), eventosController.crear);
router.get('/eventos/:id/editar', eventosController.editarForm);
router.post('/eventos/:id/editar', upload.single('imagen'), eventosController.editar);
router.post('/eventos/:id/eliminar', eventosController.eliminar);
router.post('/eventos/:id/visibilidad', eventosController.toggleVisible);

router.get('/noticias', noticiasController.index);
router.post('/noticias', upload.single('imagen'), noticiasController.crear);
router.get('/noticias/:id/editar', noticiasController.editarForm);
router.post('/noticias/:id/editar', upload.single('imagen'), noticiasController.editar);
router.post('/noticias/:id/eliminar', noticiasController.eliminar);
router.post('/noticias/:id/visibilidad', noticiasController.toggleVisible);

router.get('/fotos', fotosController.index);
router.post('/fotos', upload.galeria.array('imagenes', 20), fotosController.crear);
router.get('/fotos/:id/editar', fotosController.editarForm);
router.post('/fotos/:id/editar', upload.galeria.single('imagen'), fotosController.editar);
router.post('/fotos/:id/eliminar', fotosController.eliminar);
router.post('/fotos/:id/visibilidad', fotosController.toggleVisible);
router.post('/fotos/editar-lote', fotosController.editarLote);

router.get('/equipos', equiposController.index);
router.post('/equipos', upload.single('imagen'), equiposController.crear);
router.get('/equipos/:id/editar', equiposController.editarForm);
router.post('/equipos/:id/editar', upload.single('imagen'), equiposController.editar);
router.post('/equipos/:id/eliminar', equiposController.eliminar);
router.post('/equipos/:id/visibilidad', equiposController.toggleVisible);

router.get('/campeonatos', campeonatosController.index);
router.post('/campeonatos', campeonatosController.crear);
router.get('/campeonatos/:id/editar', campeonatosController.editarForm);
router.post('/campeonatos/:id/editar', campeonatosController.editar);
router.post('/campeonatos/:id/eliminar', campeonatosController.eliminar);

router.get('/resultados', resultadosController.index);
router.post('/resultados', resultadosController.crear);
router.get('/resultados/:id/editar', resultadosController.editarForm);
router.post('/resultados/:id/editar', resultadosController.editar);
router.post('/resultados/:id/eliminar', resultadosController.eliminar);

router.get('/estudiantes', estudiantesController.index);
router.post('/estudiantes', upload.single('imagen'), estudiantesController.crear);
router.get('/estudiantes/:id/editar', estudiantesController.editarForm);
router.post('/estudiantes/:id/editar', upload.single('imagen'), estudiantesController.editar);
router.post('/estudiantes/:id/eliminar', estudiantesController.eliminar);

router.get('/mejores-puestos', mejoresPuestosController.index);
router.post('/mejores-puestos', mejoresPuestosController.crear);
router.get('/mejores-puestos/:id/editar', mejoresPuestosController.editarForm);
router.post('/mejores-puestos/:id/editar', mejoresPuestosController.editar);
router.post('/mejores-puestos/:id/eliminar', mejoresPuestosController.eliminar);

router.get('/institucion', institucionController.index);
router.post('/institucion', upload.institucion.fields([
    { name: 'escudo', maxCount: 1 },
    { name: 'bandera', maxCount: 1 },
    { name: 'fondo', maxCount: 1 },
    { name: 'logo', maxCount: 1 },
    { name: 'instagram_imagen', maxCount: 1 },
    { name: 'facebook_imagen', maxCount: 1 },
    { name: 'plataforma_virtual_logo', maxCount: 1 },
    { name: 'manual_convivencia', maxCount: 1 },
    { name: 'manual_convivencia_imagen', maxCount: 1 },
]), institucionController.actualizar);

router.get('/mensajes', mensajesController.index);
router.post('/mensajes/:id/leido', mensajesController.marcarLeido);
router.post('/mensajes/:id/eliminar', mensajesController.eliminar);

router.get('/grados', gradosController.index);
router.post('/grados', gradosController.crear);
router.get('/grados/:id/editar', gradosController.editarForm);
router.post('/grados/:id/editar', gradosController.editar);
router.post('/grados/:id/eliminar', gradosController.eliminar);

router.get('/deportes', deportesController.index);
router.post('/deportes', upload.single('imagen'), deportesController.crear);
router.get('/deportes/:id/editar', deportesController.editarForm);
router.post('/deportes/:id/editar', upload.single('imagen'), deportesController.editar);
router.post('/deportes/:id/eliminar', deportesController.eliminar);
router.post('/deportes/:id/visibilidad', deportesController.toggleVisible);

router.get('/media-tecnica', mediaTecnicaController.index);
router.post('/media-tecnica', upload.single('imagen'), mediaTecnicaController.crear);
router.get('/media-tecnica/:id/editar', mediaTecnicaController.editarForm);
router.post('/media-tecnica/:id/editar', upload.single('imagen'), mediaTecnicaController.editar);
router.post('/media-tecnica/:id/eliminar', mediaTecnicaController.eliminar);
router.post('/media-tecnica/:id/visibilidad', mediaTecnicaController.toggleVisible);

router.get('/grupos-estudiantiles', gruposEstudiantilesController.index);
router.post('/grupos-estudiantiles', upload.single('imagen'), gruposEstudiantilesController.crear);
router.get('/grupos-estudiantiles/:id/editar', gruposEstudiantilesController.editarForm);
router.post('/grupos-estudiantiles/:id/editar', upload.single('imagen'), gruposEstudiantilesController.editar);
router.post('/grupos-estudiantiles/:id/eliminar', gruposEstudiantilesController.eliminar);
router.post('/grupos-estudiantiles/:id/visibilidad', gruposEstudiantilesController.toggleVisible);

router.get('/comunidad-educativa', comunidadController.index);
router.post('/comunidad-educativa', upload.single('imagen'), comunidadController.crear);
router.get('/comunidad-educativa/:id/editar', comunidadController.editarForm);
router.post('/comunidad-educativa/:id/editar', upload.single('imagen'), comunidadController.editar);
router.post('/comunidad-educativa/:id/eliminar', comunidadController.eliminar);
router.post('/comunidad-educativa/:id/visibilidad', comunidadController.toggleVisible);

router.get('/icfes', icfesController.index);
router.post('/icfes', upload.single('imagen'), icfesController.crear);
router.get('/icfes/:id/editar', icfesController.editarForm);
router.post('/icfes/:id/editar', upload.single('imagen'), icfesController.editar);
router.post('/icfes/:id/eliminar', icfesController.eliminar);
router.post('/icfes/:id/visibilidad', icfesController.toggleVisible);

router.get('/alianzas', alianzasController.index);
router.post('/alianzas', upload.single('imagen'), alianzasController.crear);
router.get('/alianzas/:id/editar', alianzasController.editarForm);
router.post('/alianzas/:id/editar', upload.single('imagen'), alianzasController.editar);
router.post('/alianzas/:id/eliminar', alianzasController.eliminar);
router.post('/alianzas/:id/visibilidad', alianzasController.toggleVisible);

router.get('/gobierno-escolar', gobiernoEscolarController.index);
router.post('/gobierno-escolar', upload.single('imagen'), gobiernoEscolarController.crear);
router.get('/gobierno-escolar/:id/editar', gobiernoEscolarController.editarForm);
router.post('/gobierno-escolar/:id/editar', upload.single('imagen'), gobiernoEscolarController.editar);
router.post('/gobierno-escolar/:id/eliminar', gobiernoEscolarController.eliminar);
router.post('/gobierno-escolar/:id/visibilidad', gobiernoEscolarController.toggleVisible);

router.get('/equipo-desarrollo', equipoDesarrolloController.index);
router.post('/equipo-desarrollo', upload.single('imagen'), equipoDesarrolloController.crear);
router.get('/equipo-desarrollo/:id/editar', equipoDesarrolloController.editarForm);
router.post('/equipo-desarrollo/:id/editar', upload.single('imagen'), equipoDesarrolloController.editar);
router.post('/equipo-desarrollo/:id/eliminar', equipoDesarrolloController.eliminar);
router.post('/equipo-desarrollo/:id/visibilidad', equipoDesarrolloController.toggleVisible);

router.get('/comite-ecologico', comiteEcologicoController.index);
router.post('/comite-ecologico', upload.single('imagen'), comiteEcologicoController.crear);
router.get('/comite-ecologico/:id/editar', comiteEcologicoController.editarForm);
router.post('/comite-ecologico/:id/editar', upload.single('imagen'), comiteEcologicoController.editar);
router.post('/comite-ecologico/:id/eliminar', comiteEcologicoController.eliminar);
router.post('/comite-ecologico/:id/visibilidad', comiteEcologicoController.toggleVisible);

router.get('/equipo-drones', equipoDronesController.index);
router.post('/equipo-drones', upload.single('imagen'), equipoDronesController.crear);
router.get('/equipo-drones/:id/editar', equipoDronesController.editarForm);
router.post('/equipo-drones/:id/editar', upload.single('imagen'), equipoDronesController.editar);
router.post('/equipo-drones/:id/eliminar', equipoDronesController.eliminar);
router.post('/equipo-drones/:id/visibilidad', equipoDronesController.toggleVisible);

router.get('/coheteria', coheteriaController.index);
router.post('/coheteria', upload.single('imagen'), coheteriaController.crear);
router.get('/coheteria/:id/editar', coheteriaController.editarForm);
router.post('/coheteria/:id/editar', upload.single('imagen'), coheteriaController.editar);
router.post('/coheteria/:id/eliminar', coheteriaController.eliminar);
router.post('/coheteria/:id/visibilidad', coheteriaController.toggleVisible);

module.exports = router;
