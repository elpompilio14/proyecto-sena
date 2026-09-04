document.addEventListener('DOMContentLoaded', function () {
    const elementos = Array.from(document.querySelectorAll('.mural img, .mural video'));
    if (elementos.length === 0) return;

    const overlay = document.createElement('div');
    overlay.className = 'lightbox-overlay';
    overlay.innerHTML =
        '<button type="button" class="lightbox-cerrar" aria-label="Cerrar">&times;</button>' +
        '<button type="button" class="lightbox-anterior" aria-label="Foto anterior">&#8249;</button>' +
        '<div class="lightbox-contenido"></div>' +
        '<button type="button" class="lightbox-siguiente" aria-label="Foto siguiente">&#8250;</button>' +
        '<div class="lightbox-contador"></div>';
    document.body.appendChild(overlay);

    const contenedor = overlay.querySelector('.lightbox-contenido');
    const contadorEl = overlay.querySelector('.lightbox-contador');
    let indiceActual = 0;

    function detenerVideoActual() {
        const video = contenedor.querySelector('video');
        if (video) video.pause();
    }

    function mostrar(indice) {
        detenerVideoActual();
        indiceActual = (indice + elementos.length) % elementos.length;
        const original = elementos[indiceActual];
        const url = original.dataset.url || original.src;
        contenedor.innerHTML = '';

        if (original.tagName === 'VIDEO') {
            const video = document.createElement('video');
            video.src = url;
            video.controls = true;
            video.autoplay = true;
            video.className = 'lightbox-video';
            contenedor.appendChild(video);
        } else {
            const img = document.createElement('img');
            img.src = url;
            img.alt = original.alt || '';
            img.className = 'lightbox-imagen';
            contenedor.appendChild(img);
        }

        contadorEl.textContent = (indiceActual + 1) + ' / ' + elementos.length;
    }

    function abrir(indice) {
        mostrar(indice);
        overlay.classList.add('activo');
    }

    function cerrar() {
        detenerVideoActual();
        overlay.classList.remove('activo');
    }

    elementos.forEach(function (el, indice) {
        const clicable = el.closest('.miniatura-video') || el;
        clicable.style.cursor = 'zoom-in';
        clicable.addEventListener('click', function () { abrir(indice); });
    });

    overlay.querySelector('.lightbox-cerrar').addEventListener('click', cerrar);
    overlay.querySelector('.lightbox-anterior').addEventListener('click', function () { mostrar(indiceActual - 1); });
    overlay.querySelector('.lightbox-siguiente').addEventListener('click', function () { mostrar(indiceActual + 1); });

    overlay.addEventListener('click', function (evento) {
        if (evento.target === overlay) cerrar();
    });

    document.addEventListener('keydown', function (evento) {
        if (!overlay.classList.contains('activo')) return;
        if (evento.key === 'Escape') cerrar();
        if (evento.key === 'ArrowLeft') mostrar(indiceActual - 1);
        if (evento.key === 'ArrowRight') mostrar(indiceActual + 1);
    });
});
