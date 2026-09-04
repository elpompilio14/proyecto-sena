document.addEventListener('DOMContentLoaded', function () {
    const boton = document.querySelector('.volver-arriba');
    if (!boton) return;

    function actualizarVisibilidad() {
        boton.classList.toggle('visible', window.scrollY > 400);
    }

    window.addEventListener('scroll', actualizarVisibilidad, { passive: true });
    actualizarVisibilidad();

    boton.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
