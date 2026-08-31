document.addEventListener('DOMContentLoaded', function () {
    const campos = Array.from(document.querySelectorAll('input[type="file"][data-recorte]'));
    if (campos.length === 0 || typeof Cropper === 'undefined') return;

    const overlay = document.createElement('div');
    overlay.className = 'recorte-overlay';
    overlay.innerHTML =
        '<div class="recorte-modal">' +
            '<h3>Ajusta tu foto</h3>' +
            '<p class="recorte-ayuda">Arrastra la foto y usa la rueda del mouse (o pellizca) para acomodarla.</p>' +
            '<div class="recorte-imagen-wrap"><img id="recorte-imagen-editar" alt=""></div>' +
            '<div class="recorte-botones">' +
                '<button type="button" class="btn-secondary recorte-cancelar">Cancelar</button>' +
                '<button type="button" class="recorte-confirmar">Usar esta foto</button>' +
            '</div>' +
        '</div>';
    document.body.appendChild(overlay);

    const imgEditar = overlay.querySelector('#recorte-imagen-editar');
    const btnCancelar = overlay.querySelector('.recorte-cancelar');
    const btnConfirmar = overlay.querySelector('.recorte-confirmar');

    let cropper = null;
    let campoActivo = null;

    function cerrar(limpiarCampo) {
        if (limpiarCampo && campoActivo) campoActivo.value = '';
        overlay.classList.remove('activo');
        overlay.classList.remove('recorte-circulo');
        if (cropper) { cropper.destroy(); cropper = null; }
        imgEditar.src = '';
        campoActivo = null;
    }

    campos.forEach(function (campo) {
        campo.addEventListener('change', function () {
            const archivo = campo.files && campo.files[0];
            if (!archivo) return;

            const forma = campo.dataset.recorte; // 'circulo' o 'rectangulo'
            const aspecto = campo.dataset.recorteAspecto ? Number(campo.dataset.recorteAspecto) : NaN;

            const lector = new FileReader();
            lector.onload = function (evento) {
                campoActivo = campo;
                imgEditar.src = evento.target.result;
                overlay.classList.toggle('recorte-circulo', forma === 'circulo');
                overlay.classList.add('activo');

                if (cropper) cropper.destroy();
                cropper = new Cropper(imgEditar, {
                    aspectRatio: isNaN(aspecto) ? NaN : aspecto,
                    viewMode: 1,
                    dragMode: 'move',
                    autoCropArea: 1,
                    background: false,
                    guides: false,
                    center: false,
                });
            };
            lector.readAsDataURL(archivo);
        });
    });

    btnCancelar.addEventListener('click', function () { cerrar(true); });

    overlay.addEventListener('click', function (evento) {
        if (evento.target === overlay) cerrar(true);
    });

    document.addEventListener('keydown', function (evento) {
        if (overlay.classList.contains('activo') && evento.key === 'Escape') cerrar(true);
    });

    btnConfirmar.addEventListener('click', function () {
        if (!cropper || !campoActivo) return;
        const campo = campoActivo;
        const nombreOriginal = campo.files[0] ? campo.files[0].name.replace(/\.[^.]+$/, '') : 'foto';

        cropper.getCroppedCanvas({ imageSmoothingQuality: 'high' }).toBlob(function (blob) {
            if (!blob) { cerrar(false); return; }
            const archivoRecortado = new File([blob], nombreOriginal + '.jpg', { type: 'image/jpeg' });
            const transferencia = new DataTransfer();
            transferencia.items.add(archivoRecortado);
            campo.files = transferencia.files;
            cerrar(false);
        }, 'image/jpeg', 0.92);
    });
});
