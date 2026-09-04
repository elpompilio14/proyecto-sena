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
            slide.classList.remove('primera-animada');
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

    // La primera foto arranca su zoom sola, con una animacion CSS (para que corra
    // desde el primer instante, sin parpadeo ni espera). Cuando esa animacion termina
    // del todo, recien ahi se pasa al mismo sistema de las demas fotos (clase "activa",
    // con transicion) y arranca la rotacion normal del carrusel. Si se empezara a rotar
    // antes de que la animacion terminara, se veria un corte feo a mitad del zoom.
    slides[0].addEventListener('animationend', function () {
        slides[0].classList.remove('primera-animada');
        slides[0].classList.add('activa');
        reiniciarTemporizador();
    }, { once: true });
});
