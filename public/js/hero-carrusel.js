document.addEventListener('DOMContentLoaded', function () {
    const carrusel = document.querySelector('.hero-carrusel');
    if (!carrusel) return;

    const slides = carrusel.querySelectorAll('.hero-slide');
    const dots = carrusel.querySelectorAll('.hero-dot');
    if (slides.length < 2) return;

    let actual = 0;
    let temporizador;

    function mostrar(indice) {
        slides.forEach(function (slide, i) {
            slide.classList.toggle('activa', i === indice);
        });
        dots.forEach(function (dot, i) {
            dot.classList.toggle('activo', i === indice);
        });
        actual = indice;
    }

    function reiniciarTemporizador() {
        clearInterval(temporizador);
        temporizador = setInterval(function () {
            mostrar((actual + 1) % slides.length);
        }, 7000);
    }

    dots.forEach(function (dot, i) {
        dot.addEventListener('click', function () {
            mostrar(i);
            reiniciarTemporizador();
        });
    });

    // Fuerza al navegador a aplicar los estilos iniciales (sin zoom) antes de
    // activar la primera foto, para que ese cambio si dispare la transicion de zoom
    // (si no, el navegador la pinta directamente con el zoom ya puesto).
    slides.forEach(function (slide) { slide.classList.add('entrada-rapida'); });
    void carrusel.offsetWidth;
    mostrar(0);
    reiniciarTemporizador();

    // Despues de que la primera foto ya aparecio rapido, se quita la entrada rapida
    // para que los siguientes cambios de foto usen el cruce normal, mas lento y suave.
    setTimeout(function () {
        slides.forEach(function (slide) { slide.classList.remove('entrada-rapida'); });
    }, 500);
});
