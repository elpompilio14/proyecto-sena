/* Tarjetas estilo FIFA (jugadores de cada deporte) y tarjetas de los grupos (Comite Ecologico,
   Gobierno Escolar, Equipo de Desarrollo, Equipo de Drones y Coheteria):
   - pestanas de grado y salon en la pagina del deporte
   - al pasar el mouse la tarjeta se levanta, se inclina hacia el cursor y brilla
   - al hacer clic se agranda en el centro de la pantalla
   - al hacer clic otra vez se da la vuelta y muestra la frase */
document.addEventListener('DOMContentLoaded', function () {
    // ---------- Pestanas (grados y salones) ----------
    document.querySelectorAll('[role="tablist"]').forEach(function (lista) {
        const botones = Array.from(lista.querySelectorAll(':scope > [data-pestana]'));
        botones.forEach(function (boton) {
            boton.addEventListener('click', function () {
                botones.forEach(function (b) {
                    const activo = b === boton;
                    b.classList.toggle('activo', activo);
                    b.setAttribute('aria-selected', activo ? 'true' : 'false');
                    const panel = document.querySelector('[data-panel="' + b.dataset.pestana + '"]');
                    if (panel) panel.hidden = !activo;
                });
                // Las tarjetas que aparecen en una pestana recien abierta se muestran de una vez
                const panel = document.querySelector('[data-panel="' + boton.dataset.pestana + '"]');
                if (panel) panel.querySelectorAll('.aparece').forEach(function (el) { el.classList.add('visible'); });
            });
        });
    });

    // ---------- Inclinacion hacia el cursor ----------
    const conMouse = window.matchMedia('(hover: hover)').matches;
    const sinMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (conMouse && !sinMovimiento) {
        document.querySelectorAll('.tarjeta-fifa').forEach(function (tarjeta) {
            tarjeta.addEventListener('mousemove', function (e) {
                const caja = tarjeta.getBoundingClientRect();
                const x = (e.clientX - caja.left) / caja.width - 0.5;
                const y = (e.clientY - caja.top) / caja.height - 0.5;
                tarjeta.style.setProperty('--incl-x', (-y * 14).toFixed(1) + 'deg');
                tarjeta.style.setProperty('--incl-y', (x * 16).toFixed(1) + 'deg');
                tarjeta.style.setProperty('--brillo-x', ((x + 0.5) * 100).toFixed(0) + '%');
            });
            tarjeta.addEventListener('mouseleave', function () {
                tarjeta.style.removeProperty('--incl-x');
                tarjeta.style.removeProperty('--incl-y');
                tarjeta.style.removeProperty('--brillo-x');
            });
        });
    }

    // ---------- Tarjeta agrandada ----------
    const fondo = document.createElement('div');
    fondo.className = 'tarjeta-zoom-fondo';
    fondo.hidden = true;
    fondo.innerHTML =
        '<button type="button" class="tarjeta-zoom-cerrar" aria-label="Cerrar">&times;</button>' +
        '<div class="tarjeta-zoom-escenario"></div>' +
        '<p class="tarjeta-zoom-ayuda">Toca la tarjeta para darle la vuelta</p>';
    document.body.appendChild(fondo);
    const escenario = fondo.querySelector('.tarjeta-zoom-escenario');
    let origen = null;

    function crearElemento(etiqueta, clase, texto) {
        const el = document.createElement(etiqueta);
        if (clase) el.className = clase;
        if (texto) el.textContent = texto;
        return el;
    }

    function dato(etiqueta, valor) {
        const fila = crearElemento('span', 'tarjeta-fifa-dato' + (etiqueta ? '' : ' tarjeta-fifa-dato--solo'));
        if (etiqueta) fila.appendChild(crearElemento('span', 'tarjeta-fifa-etiqueta', etiqueta));
        fila.appendChild(crearElemento('span', 'tarjeta-fifa-valor', valor));
        return fila;
    }

    // Tarjeta de un integrante de un grupo (Comite, Drones, Coheteria...), armada con los datos de su
    // tarjeta en la piramide. El color, icono, lema y frase por defecto vienen del grupo (data-tarjeta-*).
    function tarjetaGrupo(origenEl) {
        const d = origenEl.dataset;
        const piramide = origenEl.closest('[data-tarjeta-grupo]');
        const g = piramide ? piramide.dataset : {};
        const icono = g.tarjetaIcono || '⭐';
        const tarjeta = crearElemento('button', 'tarjeta-fifa tarjeta-fifa--grupo' + (g.tarjetaVariante ? ' tarjeta-fifa--' + g.tarjetaVariante : ''));
        tarjeta.type = 'button';
        const giro = crearElemento('span', 'tarjeta-fifa-giro');

        const frente = crearElemento('span', 'tarjeta-fifa-cara tarjeta-fifa-frente');
        frente.appendChild(crearElemento('span', 'tarjeta-fifa-banda', g.tarjetaGrupo || ''));
        const foto = crearElemento('span', 'tarjeta-fifa-foto');
        if (d.foto) {
            const img = document.createElement('img');
            img.src = d.foto;
            img.alt = d.nombre;
            foto.appendChild(img);
        } else {
            foto.appendChild(crearElemento('span', 'tarjeta-fifa-sin-foto', icono));
        }
        foto.appendChild(crearElemento('span', 'tarjeta-fifa-insignia', icono));
        frente.appendChild(foto);
        frente.appendChild(crearElemento('span', 'tarjeta-fifa-nombre', d.nombre));
        frente.appendChild(crearElemento('span', 'tarjeta-fifa-rol', d.rol || 'Integrante'));

        // Filas que el admin escribio ("Cargo: Docente"); las vacias no salen
        let filas = [];
        try { filas = JSON.parse(d.datos || '[]'); } catch (err) { filas = []; }
        filas = filas.filter(function (f) { return f && f[1]; });
        if (filas.length) {
            const datos = crearElemento('span', 'tarjeta-fifa-datos');
            filas.forEach(function (f) { datos.appendChild(dato(f[0], f[1])); });
            frente.appendChild(datos);
        }
        if (g.tarjetaLema) frente.appendChild(crearElemento('span', 'tarjeta-fifa-lema', icono + ' ' + g.tarjetaLema));

        const reverso = crearElemento('span', 'tarjeta-fifa-cara tarjeta-fifa-reverso');
        reverso.appendChild(crearElemento('span', 'tarjeta-fifa-comillas', '“'));
        reverso.appendChild(crearElemento('span', 'tarjeta-fifa-frase', d.frase || g.tarjetaFrase || ''));
        reverso.appendChild(crearElemento('span', 'tarjeta-fifa-firma', '— ' + d.nombre));
        reverso.appendChild(crearElemento('span', 'tarjeta-fifa-icono-reverso', icono));

        giro.appendChild(frente);
        giro.appendChild(reverso);
        tarjeta.appendChild(giro);
        return tarjeta;
    }

    function abrir(origenEl) {
        origen = origenEl;
        let tarjeta;
        if (origenEl.classList.contains('tarjeta-fifa')) {
            tarjeta = origenEl.cloneNode(true);
            tarjeta.classList.remove('aparece', 'visible');
            tarjeta.removeAttribute('style');
            tarjeta.querySelectorAll('img').forEach(function (img) { img.loading = 'eager'; });
        } else {
            tarjeta = tarjetaGrupo(origenEl);
        }
        tarjeta.classList.add('tarjeta-fifa--zoom');
        tarjeta.setAttribute('aria-label', 'Dar la vuelta a la tarjeta');
        tarjeta.addEventListener('click', function (e) {
            e.stopPropagation();
            tarjeta.classList.toggle('volteada');
        });

        escenario.innerHTML = '';
        escenario.appendChild(tarjeta);
        fondo.hidden = false;
        document.body.classList.add('tarjeta-zoom-abierta');
        requestAnimationFrame(function () { fondo.classList.add('abierto'); });
        tarjeta.focus({ preventScroll: true });
    }

    function cerrar() {
        if (fondo.hidden) return;
        fondo.classList.remove('abierto');
        document.body.classList.remove('tarjeta-zoom-abierta');
        setTimeout(function () {
            fondo.hidden = true;
            escenario.innerHTML = '';
        }, 250);
        if (origen) origen.focus({ preventScroll: true });
        origen = null;
    }

    fondo.addEventListener('click', function (e) {
        if (!e.target.closest('.tarjeta-fifa--zoom')) cerrar();
    });
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') cerrar();
    });

    document.querySelectorAll('.tarjeta-fifa').forEach(function (tarjeta) {
        tarjeta.addEventListener('click', function () { abrir(tarjeta); });
    });
    document.querySelectorAll('.tarjeta-volteable').forEach(function (tarjeta) {
        tarjeta.addEventListener('click', function () { abrir(tarjeta); });
        tarjeta.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                abrir(tarjeta);
            }
        });
    });
});
