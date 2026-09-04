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

    requestAnimationFrame(function () {
        requestAnimationFrame(function () {
            mostrar(0);
            reiniciarTemporizador();
        });
    });
});
