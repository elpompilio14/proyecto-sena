/* Agrega un "ojito" a la derecha de cada campo de contrasena (iniciar sesion, registrarse,
   restablecer contrasena...) para mostrar u ocultar lo que se escribio. */
document.addEventListener('DOMContentLoaded', function () {
    const OJO_ABIERTO =
        '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7Z"/><circle cx="12" cy="12" r="3"/></svg>';
    const OJO_TACHADO =
        '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M9.9 4.2A10.8 10.8 0 0 1 12 4c7 0 11 8 11 8a18.4 18.4 0 0 1-2.2 3.2"/>' +
        '<path d="M6.6 6.6A18.5 18.5 0 0 0 1 12s4 8 11 8a10.9 10.9 0 0 0 5.4-1.4"/>' +
        '<path d="M14.1 14.1a3 3 0 1 1-4.2-4.2"/><line x1="1" y1="1" x2="23" y2="23"/></svg>';

    document.querySelectorAll('input[type="password"]').forEach(function (campo) {
        // El boton va en el mismo contenedor del campo; si el campo no tiene uno propio, se le crea
        let contenedor = campo.parentElement;
        if (!contenedor.classList.contains('auth-input-wrap')) {
            contenedor = document.createElement('span');
            contenedor.className = 'campo-contrasena';
            campo.parentNode.insertBefore(contenedor, campo);
            contenedor.appendChild(campo);
        }
        contenedor.classList.add('con-ver-contrasena');

        const boton = document.createElement('button');
        boton.type = 'button';
        boton.className = 'ver-contrasena';
        boton.tabIndex = 0;

        function pintar() {
            const visible = campo.type === 'text';
            boton.innerHTML = visible ? OJO_TACHADO : OJO_ABIERTO;
            boton.setAttribute('aria-label', visible ? 'Ocultar contraseña' : 'Mostrar contraseña');
            boton.title = visible ? 'Ocultar contraseña' : 'Mostrar contraseña';
            boton.classList.toggle('activo', visible);
        }

        boton.addEventListener('click', function () {
            // Se guarda donde estaba el cursor para que siga escribiendo en el mismo lugar
            const inicio = campo.selectionStart;
            const fin = campo.selectionEnd;
            campo.type = campo.type === 'password' ? 'text' : 'password';
            pintar();
            campo.focus();
            try { campo.setSelectionRange(inicio, fin); } catch (e) { /* algunos navegadores no lo permiten */ }
        });

        // Al enviar el formulario se vuelve a ocultar (para que el navegador no la guarde como texto)
        if (campo.form) {
            campo.form.addEventListener('submit', function () { campo.type = 'password'; });
        }

        pintar();
        contenedor.appendChild(boton);
    });
});
