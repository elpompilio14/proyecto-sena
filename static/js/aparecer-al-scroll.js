document.addEventListener('DOMContentLoaded', function () {
    const elementos = document.querySelectorAll('.aparece');
    if (elementos.length === 0) return;

    if (!('IntersectionObserver' in window)) {
        elementos.forEach(function (el) { el.classList.add('visible'); });
        return;
    }

    const observador = new IntersectionObserver(function (entradas) {
        entradas.forEach(function (entrada) {
            if (entrada.isIntersecting) {
                entrada.target.classList.add('visible');
                observador.unobserve(entrada.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    elementos.forEach(function (el) { observador.observe(el); });
});
