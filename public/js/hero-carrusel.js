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

    // La primera foto ya sale visible desde el HTML (sin parpadeo azul, pase lo que
    // pase con el JS a continuacion), pero todavia sin zoom. Se espera a que el
    // navegador pinte esa version (dos requestAnimationFrame, para asegurar un pintado
    // real de por medio) y recien ahi se activa el zoom con "activa": el mismo
    // mecanismo (transicion) que usan todas las demas fotos, sin mezclarlo con
    // animaciones aparte, que era lo que causaba el corte al pasar a la siguiente foto.
    requestAnimationFrame(function () {
        requestAnimationFrame(function () {
            slides[0].classList.remove('visible-estatica');
            mostrar(0);
            reiniciarTemporizador();
        });
    });
});
