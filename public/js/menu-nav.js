document.addEventListener('DOMContentLoaded', function () {
    var boton = document.getElementById('btn-hamburguesa');
    var nav = document.getElementById('nav-principal');

    if (boton && nav) {
        boton.addEventListener('click', function () {
            var abierto = nav.classList.toggle('nav-abierto');
            boton.classList.toggle('activo', abierto);
            boton.setAttribute('aria-expanded', abierto ? 'true' : 'false');
        });
    }

    document.querySelectorAll('.nav-dropdown-btn').forEach(function (boton) {
        boton.addEventListener('click', function (evento) {
            evento.stopPropagation();
            var contenedor = boton.closest('.nav-dropdown');
            var yaAbierto = contenedor.classList.contains('abierto');
            document.querySelectorAll('.nav-dropdown.abierto').forEach(function (otro) {
                if (otro !== contenedor) otro.classList.remove('abierto');
            });
            contenedor.classList.toggle('abierto', !yaAbierto);
        });
    });

    document.addEventListener('click', function (evento) {
        document.querySelectorAll('.nav-dropdown.abierto').forEach(function (contenedor) {
            if (!contenedor.contains(evento.target)) {
                contenedor.classList.remove('abierto');
            }
        });
    });
});
