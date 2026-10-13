document.addEventListener('DOMContentLoaded', function () {
    const carrusel = document.querySelector('.hero-carrusel');
    if (!carrusel) return;

    const slides = carrusel.querySelectorAll('.hero-slide');
    const dots = carrusel.querySelectorAll('.hero-dot');
    const anterior = carrusel.querySelector('.hero-flecha-anterior');
    const siguiente = carrusel.querySelector('.hero-flecha-siguiente');
    if (slides.length < 2) return;

    const DURACION = 1100; // ms que tarda una foto en deslizarse
    const ESPERA = 5000;   // ms que se queda cada foto antes de pasar sola
    const CURVA = 'cubic-bezier(.77, 0, .18, 1)';
    const sinMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    let actual = 0;
    let animando = false;
    let temporizador;

    // Posicion fuera de la caja: dir = 1 a la derecha, -1 a la izquierda
    function fuera(dir) {
        return 'translateX(calc(' + dir + ' * (100% + var(--hero-separacion))))';
    }

    function marcarActiva(indice) {
        slides.forEach(function (slide, i) {
            slide.classList.toggle('activa', i === indice);
            slide.setAttribute('aria-hidden', i === indice ? 'false' : 'true');
            slide.querySelectorAll('a').forEach(function (a) {
                a.tabIndex = i === indice ? 0 : -1;
            });
        });
        dots.forEach(function (dot, i) {
            dot.classList.toggle('activo', i === indice);
        });
    }

    // dir = 1: la nueva entra por la derecha (avanzar); -1: entra por la izquierda
    function ir(nuevo, dir) {
        if (animando || nuevo === actual) return;
        const sale = slides[actual];
        const entra = slides[nuevo];
        // La animacion de bienvenida de la primera foto ya no hace falta
        slides.forEach(function (s) { s.classList.remove('hero-inicial'); });

        if (sinMovimiento) {
            actual = nuevo;
            marcarActiva(nuevo);
            return;
        }

        animando = true;

        // 1) Poner la que entra afuera, sin animacion
        entra.style.transition = 'none';
        entra.style.transform = fuera(dir);
        entra.style.opacity = '0.4';
        entra.classList.add('moviendo');
        sale.classList.add('moviendo');
        void entra.offsetWidth; // obliga al navegador a aplicar esa posicion antes de animar

        // 2) Deslizar las dos a la vez
        const transicion = 'transform ' + DURACION + 'ms ' + CURVA + ', opacity ' + DURACION + 'ms ease';
        entra.style.transition = transicion;
        sale.style.transition = transicion;
        entra.style.transform = 'translateX(0)';
        entra.style.opacity = '1';
        sale.style.transform = fuera(-dir);
        sale.style.opacity = '0.4';

        actual = nuevo;
        marcarActiva(nuevo);

        // 3) Al terminar, limpiar estilos sueltos
        setTimeout(function () {
            [entra, sale].forEach(function (s) {
                s.classList.remove('moviendo');
                s.style.transition = '';
                s.style.transform = '';
                s.style.opacity = '';
            });
            animando = false;
        }, DURACION + 30);
    }

    function avanzar() { ir((actual + 1) % slides.length, 1); }
    function retroceder() { ir((actual - 1 + slides.length) % slides.length, -1); }

    function reiniciarTemporizador() {
        clearInterval(temporizador);
        temporizador = setInterval(avanzar, ESPERA);
    }

    function pausar() { clearInterval(temporizador); }

    siguiente.addEventListener('click', function () { avanzar(); reiniciarTemporizador(); });
    anterior.addEventListener('click', function () { retroceder(); reiniciarTemporizador(); });

    dots.forEach(function (dot, i) {
        dot.addEventListener('click', function () {
            ir(i, i > actual ? 1 : -1);
            reiniciarTemporizador();
        });
    });

    // Flechas del teclado cuando el foco esta dentro del carrusel
    carrusel.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') { avanzar(); reiniciarTemporizador(); }
        if (e.key === 'ArrowLeft') { retroceder(); reiniciarTemporizador(); }
    });

    // Deslizar con el dedo en el celular
    let inicioX = null;
    let inicioY = null;
    carrusel.addEventListener('touchstart', function (e) {
        inicioX = e.touches[0].clientX;
        inicioY = e.touches[0].clientY;
        pausar();
    }, { passive: true });
    carrusel.addEventListener('touchend', function (e) {
        if (inicioX !== null) {
            const dx = e.changedTouches[0].clientX - inicioX;
            const dy = e.changedTouches[0].clientY - inicioY;
            if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) {
                if (dx < 0) avanzar(); else retroceder();
            }
        }
        inicioX = null;
        reiniciarTemporizador();
    });

    marcarActiva(0);
    reiniciarTemporizador();

    // Cuando termina la animacion de bienvenida, la primera foto queda como cualquier otra
    setTimeout(function () {
        if (!animando) slides[0].classList.remove('hero-inicial');
    }, 1900);
});
