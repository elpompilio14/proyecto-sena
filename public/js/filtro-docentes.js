document.addEventListener('DOMContentLoaded', function () {
    var botones = document.querySelectorAll('.docentes-filtro-btn');
    var tarjetas = document.querySelectorAll('.docente-card');
    if (botones.length === 0) return;

    botones.forEach(function (boton) {
        boton.addEventListener('click', function () {
            botones.forEach(function (b) { b.classList.remove('activo'); });
            boton.classList.add('activo');
            var area = boton.getAttribute('data-area');
            tarjetas.forEach(function (tarjeta) {
                var mostrar = area === 'todos' || tarjeta.getAttribute('data-area') === area;
                tarjeta.style.display = mostrar ? '' : 'none';
            });
        });
    });
});
