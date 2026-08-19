const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

router.get('/registro', authController.registroForm);
router.post('/registro', authController.registro);
router.get('/login', authController.loginForm);
router.post('/login', authController.login);
router.post('/logout', authController.logout);

router.get('/verificar-correo', authController.verificarForm);
router.post('/verificar-correo', authController.verificar);
router.post('/verificar-correo/reenviar', authController.reenviarCodigo);

router.get('/auth/google', authController.iniciarGoogle);
router.get('/auth/google/callback', authController.callbackGoogle);

module.exports = router;
