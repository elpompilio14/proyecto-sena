const express = require('express');
const router = express.Router();
const publicController = require('../controllers/publicController');

router.get('/', publicController.home);
router.get('/institucion', publicController.institucion);
router.get('/comunidad-educativa', publicController.comunidadEducativa);
router.get('/himno', publicController.himno);
router.get('/noticias', publicController.noticias);
router.get('/noticias/:id', publicController.noticiaDetalle);
router.get('/eventos', publicController.eventos);
router.get('/eventos/:id', publicController.eventoDetalle);
router.get('/deportes', publicController.deportes);
router.get('/campeonatos', publicController.campeonatos);
router.get('/campeonatos/:id', publicController.campeonatoDetalle);
router.get('/mejores-puestos', publicController.mejoresPuestos);
router.get('/icfes', publicController.icfes);
router.get('/galeria', publicController.galeria);
router.get('/contacto', publicController.contactoForm);
router.post('/contacto', publicController.contacto);

module.exports = router;
