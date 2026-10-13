"""Jugadores de cada deporte (tarjetas estilo FIFA en la pagina publica del deporte)."""
from flask import render_template, request, redirect, abort, jsonify
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo


def _numero(texto, tipo=int):
    """Convierte el texto del formulario a numero; si viene vacio o mal escrito devuelve None."""
    try:
        return tipo((texto or '').strip().replace(',', '.'))
    except ValueError:
        return None


def _altura(texto):
    """Acepta '1.75', '1,75' o '175' (centimetros) y la guarda en metros."""
    altura = _numero(texto, float)
    if altura is None or altura <= 0:
        return None
    if altura > 3:  # la escribieron en centimetros
        altura = altura / 100
    return round(altura, 2) if altura < 10 else None


def _datos_formulario(form, foto_url):
    return (
        form.get('grado_id') or None,
        (form.get('nombre') or '').strip(),
        foto_url,
        _altura(form.get('altura')),
        _numero(form.get('edad')),
        (form.get('posicion') or '').strip() or None,
        (form.get('frase') or '').strip() or None,
        _numero(form.get('orden')) or 0,
    )


def _grados(cur):
    cur.execute('SELECT * FROM grados ORDER BY nivel, nombre')
    return cur.fetchall()


@admin_bp.route('/deportes/<int:deporte_id>/jugadores')
def deportistas_index(deporte_id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM deportes WHERE id = %s', (deporte_id,))
            deporte = cur.fetchone()
            if not deporte:
                abort(404)
            cur.execute("""
                SELECT deportistas.*, grados.nombre AS grado_nombre
                FROM deportistas
                LEFT JOIN grados ON grados.id = deportistas.grado_id
                WHERE deportistas.deporte_id = %s
                ORDER BY grados.nivel NULLS LAST, grados.nombre, deportistas.orden, deportistas.nombre
            """, (deporte_id,))
            jugadores = cur.fetchall()
            grados = _grados(cur)
    return render_template(
        'admin/deportistas.html', titulo='Admin · Jugadores de ' + deporte['nombre'],
        deporte=deporte, jugadores=jugadores, grados=grados,
    )


@admin_bp.route('/deportes/<int:deporte_id>/jugadores', methods=['POST'])
def deportistas_crear(deporte_id):
    foto_url = guardar_archivo(request.files.get('imagen'))
    datos = _datos_formulario(request.form, foto_url)
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """INSERT INTO deportistas (deporte_id, grado_id, nombre, foto_url, altura, edad, posicion, frase, orden)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (deporte_id, *datos),
            )
    return redirect(f'/admin/deportes/{deporte_id}/jugadores')


@admin_bp.route('/jugadores/<int:id>/editar')
def deportistas_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("""
                SELECT deportistas.*, deportes.nombre AS deporte_nombre
                FROM deportistas JOIN deportes ON deportes.id = deportistas.deporte_id
                WHERE deportistas.id = %s
            """, (id,))
            jugador = cur.fetchone()
            if not jugador:
                abort(404)
            grados = _grados(cur)
    return render_template('admin/deportistas_editar.html', titulo='Admin · Editar jugador', jugador=jugador, grados=grados)


@admin_bp.route('/jugadores/<int:id>/editar', methods=['POST'])
def deportistas_editar(id):
    foto_url = guardar_archivo(request.files.get('imagen')) or (request.form.get('foto_actual') or None)
    datos = _datos_formulario(request.form, foto_url)
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """UPDATE deportistas SET grado_id = %s, nombre = %s, foto_url = %s, altura = %s, edad = %s,
                   posicion = %s, frase = %s, orden = %s WHERE id = %s RETURNING deporte_id""",
                (*datos, id),
            )
            fila = cur.fetchone()
    if not fila:
        abort(404)
    return redirect(f"/admin/deportes/{fila['deporte_id']}/jugadores")


@admin_bp.route('/jugadores/<int:id>/eliminar', methods=['POST'])
def deportistas_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM deportistas WHERE id = %s RETURNING deporte_id', (id,))
            fila = cur.fetchone()
    return redirect(f"/admin/deportes/{fila['deporte_id']}/jugadores" if fila else '/admin/deportes')


@admin_bp.route('/jugadores/<int:id>/visibilidad', methods=['POST'])
def deportistas_toggle_visible(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('UPDATE deportistas SET visible = NOT visible WHERE id = %s RETURNING visible', (id,))
            resultado = cur.fetchone()
    return jsonify({'visible': resultado['visible']})
