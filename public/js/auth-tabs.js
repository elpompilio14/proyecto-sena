document.addEventListener('DOMContentLoaded', function () {
    const pestanas = document.querySelectorAll('.auth-tab');
    if (pestanas.length === 0) return;

    pestanas.forEach(function (pestana) {
        pestana.addEventListener('click', function () {
            const objetivo = pestana.dataset.tab;

            document.querySelectorAll('.auth-tab').forEach(function (t) {
                t.classList.remove('activo');
            });
            pestana.classList.add('activo');

            document.querySelectorAll('.auth-panel').forEach(function (panel) {
                panel.classList.toggle('oculto', panel.id !== 'panel-' + objetivo);
            });
        });
    });
});
