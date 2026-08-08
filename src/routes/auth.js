const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

router.get('/registro', authController.registroForm);
router.post('/registro', authController.registro);
router.get('/login', authController.loginForm);
router.post('/login', authController.login);
router.post('/logout', authController.logout);

module.exports = router;
