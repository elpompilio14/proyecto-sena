document.addEventListener('DOMContentLoaded', function () {
    const miniaturas = Array.from(document.querySelectorAll('.tabla-foto-mini'));
    if (miniaturas.length === 0) return;

    const overlay = document.createElement('div');
    overlay.className = 'lightbox-overlay';
    overlay.innerHTML =
        '<button type="button" class="lightbox-cerrar" aria-label="Cerrar">&times;</button>' +
        '<div class="lightbox-contenido"></div>';
    document.body.appendChild(overlay);

    const contenedor = overlay.querySelector('.lightbox-contenido');

    function abrir(src, alt) {
        contenedor.innerHTML = '';
        const img = document.createElement('img');
        img.src = src;
        img.alt = alt || '';
        img.className = 'lightbox-imagen';
        contenedor.appendChild(img);
        overlay.classList.add('activo');
    }

    function cerrar() {
        overlay.classList.remove('activo');
    }

    miniaturas.forEach(function (img) {
        img.addEventListener('click', function () { abrir(img.src, img.alt); });
    });

    overlay.querySelector('.lightbox-cerrar').addEventListener('click', cerrar);
    overlay.addEventListener('click', function (evento) {
        if (evento.target === overlay) cerrar();
    });
    document.addEventListener('keydown', function (evento) {
        if (overlay.classList.contains('activo') && evento.key === 'Escape') cerrar();
    });
});
