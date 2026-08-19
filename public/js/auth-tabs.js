document.addEventListener('DOMContentLoaded', function () {
    const contenedor = document.getElementById('auth-container');
    if (!contenedor) return;

    const cajaLogin = document.getElementById('caja-login');
    const cajaRegistro = document.getElementById('caja-registro');

    function mostrarRegistro() {
        contenedor.classList.add('right-active');
        cajaLogin.classList.remove('auth-visible-mobile');
        cajaRegistro.classList.add('auth-visible-mobile');
    }

    function mostrarLogin() {
        contenedor.classList.remove('right-active');
        cajaRegistro.classList.remove('auth-visible-mobile');
        cajaLogin.classList.add('auth-visible-mobile');
    }

    document.querySelectorAll('[data-mostrar="registro"]').forEach(function (el) {
        el.addEventListener('click', function (evento) {
            evento.preventDefault();
            mostrarRegistro();
        });
    });

    document.querySelectorAll('[data-mostrar="login"]').forEach(function (el) {
        el.addEventListener('click', function (evento) {
            evento.preventDefault();
            mostrarLogin();
        });
    });
});
