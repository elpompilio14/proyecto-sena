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

    // La primera foto sale visible desde el HTML (sin fundido, para que no se vea un
    // parpadeo azul al cargar), pero todavia sin zoom. Se fuerza al navegador a aplicar
    // ese estado (reflow) y de inmediato se activa el zoom, asi arranca practicamente
    // desde el primer instante, sin demora perceptible ni parpadeo.
    void carrusel.offsetWidth;
    slides[0].classList.remove('visible-estatica');
    mostrar(0);
    reiniciarTemporizador();
});
