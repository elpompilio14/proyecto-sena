document.addEventListener('DOMContentLoaded', function () {
    const botones = Array.from(document.querySelectorAll('.toggle-visibilidad'));
    if (botones.length === 0) return;

    botones.forEach(function (boton) {
        boton.addEventListener('click', function () {
            if (boton.disabled) return;
            boton.disabled = true;
            boton.classList.add('animando');

            fetch(boton.dataset.url, { method: 'POST', headers: { 'X-Requested-With': 'fetch' } })
                .then(function (respuesta) {
                    if (!respuesta.ok) throw new Error('No se pudo cambiar la visibilidad');
                    return respuesta.json();
                })
                .then(function (datos) {
                    setTimeout(function () {
                        const visible = !!datos.visible;
                        boton.dataset.visible = visible ? 'true' : 'false';
                        boton.setAttribute('aria-label', visible ? 'Ocultar foto al público' : 'Mostrar foto al público');
                        boton.setAttribute('title', visible ? 'Se ve en el sitio público. Clic para ocultarla' : 'Oculta al público. Clic para mostrarla');
                        boton.classList.remove('animando');
                        boton.disabled = false;
                    }, 200);
                })
                .catch(function () {
                    boton.classList.remove('animando');
                    boton.disabled = false;
                    alert('No se pudo cambiar la visibilidad de la foto. Intenta de nuevo.');
                });
        });
    });
});
