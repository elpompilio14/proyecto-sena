// Pestañita para esconder / mostrar la barra fija de arriba (franja azul + menu).
// Se carga justo despues de .encabezado-fijo (no al final del body) para aplicar la
// preferencia guardada antes de que la pagina se pinte y evitar un "parpadeo".
(function () {
    var encabezado = document.querySelector('.encabezado-fijo');
    var boton = document.querySelector('.encabezado-toggle');
    if (!encabezado || !boton) return;

    var CLAVE = 'encabezadoOculto';

    function leerPreferencia() {
        try {
            return localStorage.getItem(CLAVE) === '1';
        } catch (err) {
            return false;
        }
    }

    function guardarPreferencia(oculto) {
        try {
            localStorage.setItem(CLAVE, oculto ? '1' : '0');
        } catch (err) {
            // Si el navegador no deja guardar, la pagina sigue funcionando igual.
        }
    }

    // La altura de la barra se guarda en una variable CSS para que el margen
    // negativo compense exactamente el espacio que deja al esconderse.
    function actualizarAltura() {
        encabezado.style.setProperty('--altura-encabezado', encabezado.offsetHeight + 'px');
    }

    function aplicarEstado(oculto) {
        encabezado.classList.toggle('encabezado-oculto', oculto);
        boton.setAttribute('aria-expanded', oculto ? 'false' : 'true');
        boton.setAttribute('aria-label', oculto ? 'Mostrar menú' : 'Ocultar menú');
        boton.title = oculto ? 'Mostrar menú' : 'Ocultar menú';
    }

    actualizarAltura();
    if ('ResizeObserver' in window) {
        new ResizeObserver(actualizarAltura).observe(encabezado);
    } else {
        window.addEventListener('resize', actualizarAltura);
        window.addEventListener('load', actualizarAltura);
    }

    // Estado inicial sin animacion (para que no se vea deslizar al cambiar de pagina).
    if (leerPreferencia()) {
        encabezado.classList.add('encabezado-sin-animacion');
        aplicarEstado(true);
        requestAnimationFrame(function () {
            requestAnimationFrame(function () {
                encabezado.classList.remove('encabezado-sin-animacion');
            });
        });
    } else {
        aplicarEstado(false);
    }

    boton.addEventListener('click', function () {
        var ocultar = !encabezado.classList.contains('encabezado-oculto');

        if (ocultar) {
            // Cierra el menu de celular y los desplegables antes de esconder la barra.
            var nav = document.getElementById('nav-principal');
            var hamburguesa = document.getElementById('btn-hamburguesa');
            if (nav && nav.classList.contains('nav-abierto') && hamburguesa) {
                hamburguesa.click();
            }
            document.querySelectorAll('.nav-dropdown.abierto').forEach(function (contenedor) {
                contenedor.classList.remove('abierto');
            });
        }

        aplicarEstado(ocultar);
        guardarPreferencia(ocultar);
    });
})();
