document.addEventListener('DOMContentLoaded', function () {
    const checkTodas = document.getElementById('check-todas-fotos');
    if (!checkTodas) return;

    const filas = Array.from(document.querySelectorAll('.fila-check-foto'));

    checkTodas.addEventListener('change', function () {
        filas.forEach(function (cb) { cb.checked = checkTodas.checked; });
    });
});
