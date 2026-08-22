document.addEventListener('DOMContentLoaded', function () {
    var numeros = document.querySelectorAll('.stat-numero');
    if (numeros.length === 0) return;

    var prefiereMenosMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var DURACION = 4000;

    function animarContador(elemento) {
        var meta = parseInt(elemento.getAttribute('data-meta'), 10) || 0;

        if (prefiereMenosMovimiento) {
            elemento.textContent = meta;
            return;
        }

        var inicio = null;

        function paso(marcaTiempo) {
            if (inicio === null) inicio = marcaTiempo;
            var progreso = Math.min((marcaTiempo - inicio) / DURACION, 1);
            var facilitado = 1 - Math.pow(1 - progreso, 3);
            elemento.textContent = Math.floor(facilitado * meta);
            if (progreso < 1) {
                requestAnimationFrame(paso);
            } else {
                elemento.textContent = meta;
            }
        }
        requestAnimationFrame(paso);
    }

    if ('IntersectionObserver' in window) {
        var observador = new IntersectionObserver(function (entradas) {
            entradas.forEach(function (entrada) {
                if (entrada.isIntersecting) {
                    animarContador(entrada.target);
                    observador.unobserve(entrada.target);
                }
            });
        }, { threshold: 0.4 });
        numeros.forEach(function (elemento) { observador.observe(elemento); });
    } else {
        numeros.forEach(animarContador);
    }
});
