document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('form.form').forEach(function (formulario) {
        formulario.addEventListener('submit', function () {
            const boton = formulario.querySelector('button[type="submit"]');
            if (!boton || boton.disabled) return;
            boton.disabled = true;
            boton.dataset.textoOriginal = boton.textContent;
            boton.textContent = 'Enviando...';
        });
    });
});
