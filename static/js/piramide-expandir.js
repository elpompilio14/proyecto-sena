document.addEventListener('DOMContentLoaded', function () {
    const botones = Array.from(document.querySelectorAll('.piramide-boton-expandir'));
    botones.forEach(function (boton) {
        const piramide = boton.closest('.piramide');
        if (!piramide) return;
        const ocultos = Array.from(piramide.querySelectorAll('[data-piramide-extra][hidden]'));
        const textoOriginal = boton.textContent;

        boton.addEventListener('click', function () {
            const expandido = boton.dataset.expandido === 'true';
            ocultos.forEach(function (el) { el.hidden = expandido; });
            boton.dataset.expandido = expandido ? 'false' : 'true';
            boton.textContent = expandido ? textoOriginal : 'Ver menos';
        });
    });
});
