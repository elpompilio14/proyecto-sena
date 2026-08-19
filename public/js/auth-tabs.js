document.addEventListener('DOMContentLoaded', function () {
    const contenedor = document.getElementById('auth-container');
    if (!contenedor) return;

    const cajaLogin = document.getElementById('caja-login');
    const cajaRegistro = document.getElementById('caja-registro');
    const ola = document.getElementById('auth-ola');

    // Parte el texto de cada titulo en letras individuales para animarlas una por una
    function prepararLetras(elemento) {
        const texto = elemento.textContent;
        elemento.textContent = '';
        texto.split('').forEach(function (letra) {
            const span = document.createElement('span');
            span.className = 'auth-letra';
            span.textContent = letra === ' ' ? ' ' : letra;
            elemento.appendChild(span);
        });
    }

    document.querySelectorAll('.auth-form h2').forEach(prepararLetras);

    function animarEntrada(caja) {
        const letras = caja.querySelectorAll('.auth-letra');
        const campos = caja.querySelectorAll('.auth-input-wrap, .auth-submit, .auth-google-btn, .auth-separador');

        letras.forEach(function (letra) { letra.classList.add('auth-letra-oculta'); });
        campos.forEach(function (campo) { campo.classList.add('auth-campo-oculto'); });

        // Fuerza un reflow para que el navegador registre el estado oculto antes de animar
        // (sin depender de requestAnimationFrame, que se pausa en pestañas no visibles)
        void caja.offsetWidth;

        letras.forEach(function (letra, indice) {
            letra.style.transitionDelay = (indice * 26) + 'ms';
            letra.classList.remove('auth-letra-oculta');
        });
        campos.forEach(function (campo, indice) {
            campo.style.transitionDelay = (300 + indice * 60) + 'ms';
            campo.classList.remove('auth-campo-oculto');
        });
    }

    let animando = false;

    function cambiarA(destino) {
        if (animando) return;
        animando = true;

        ola.classList.remove('auth-ola-saliendo');
        ola.classList.add('auth-ola-cubriendo');

        setTimeout(function () {
            if (destino === 'registro') {
                contenedor.classList.add('right-active');
                cajaLogin.classList.remove('auth-visible-mobile');
                cajaRegistro.classList.add('auth-visible-mobile');
            } else {
                contenedor.classList.remove('right-active');
                cajaRegistro.classList.remove('auth-visible-mobile');
                cajaLogin.classList.add('auth-visible-mobile');
            }

            setTimeout(function () {
                ola.classList.remove('auth-ola-cubriendo');
                ola.classList.add('auth-ola-saliendo');
                animarEntrada(destino === 'registro' ? cajaRegistro : cajaLogin);

                setTimeout(function () {
                    ola.classList.remove('auth-ola-saliendo');
                    animando = false;
                }, 700);
            }, 450);
        }, 550);
    }

    document.querySelectorAll('[data-mostrar="registro"]').forEach(function (el) {
        el.addEventListener('click', function (evento) {
            evento.preventDefault();
            cambiarA('registro');
        });
    });

    document.querySelectorAll('[data-mostrar="login"]').forEach(function (el) {
        el.addEventListener('click', function (evento) {
            evento.preventDefault();
            cambiarA('login');
        });
    });
});
