from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion


@admin_bp.route('/resultados')
def resultados_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("""
                SELECT resultados.*, c.nombre AS campeonato_nombre,
                       el.nombre AS equipo_local_nombre, ev.nombre AS equipo_visitante_nombre
                FROM resultados
                JOIN campeonatos c ON c.id = resultados.campeonato_id
                JOIN equipos el ON el.id = resultados.equipo_local_id
                JOIN equipos ev ON ev.id = resultados.equipo_visitante_id
                ORDER BY resultados.fecha DESC
            """)
            resultados = cur.fetchall()
            cur.execute('SELECT id, nombre FROM campeonatos ORDER BY nombre')
            campeonatos = cur.fetchall()
            cur.execute('SELECT id, nombre FROM equipos ORDER BY nombre')
            equipos = cur.fetchall()

    return render_template(
        'admin/resultados.html', titulo='Admin · Resultados', resultados=resultados, campeonatos=campeonatos, equipos=equipos,
    )


@admin_bp.route('/resultados', methods=['POST'])
def resultados_crear():
    campeonato_id = request.form.get('campeonato_id')
    equipo_local_id = request.form.get('equipo_local_id')
    equipo_visitante_id = request.form.get('equipo_visitante_id')
    marcador_local = request.form.get('marcador_local') or 0
    marcador_visitante = request.form.get('marcador_visitante') or 0
    fecha = request.form.get('fecha')

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """INSERT INTO resultados (campeonato_id, equipo_local_id, equipo_visitante_id, marcador_local, marcador_visitante, fecha)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (campeonato_id, equipo_local_id, equipo_visitante_id, marcador_local, marcador_visitante, fecha),
            )
    return redirect('/admin/resultados')


@admin_bp.route('/resultados/<int:id>/editar')
def resultados_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM resultados WHERE id = %s', (id,))
            resultado = cur.fetchone()
            if not resultado:
                abort(404)
            cur.execute('SELECT id, nombre FROM campeonatos ORDER BY nombre')
            campeonatos = cur.fetchall()
            cur.execute('SELECT id, nombre FROM equipos ORDER BY nombre')
            equipos = cur.fetchall()

    return render_template(
        'admin/resultados_editar.html', titulo='Admin · Editar resultado', resultado=resultado, campeonatos=campeonatos, equipos=equipos,
    )


@admin_bp.route('/resultados/<int:id>/editar', methods=['POST'])
def resultados_editar(id):
    campeonato_id = request.form.get('campeonato_id')
    equipo_local_id = request.form.get('equipo_local_id')
    equipo_visitante_id = request.form.get('equipo_visitante_id')
    marcador_local = request.form.get('marcador_local') or 0
    marcador_visitante = request.form.get('marcador_visitante') or 0
    fecha = request.form.get('fecha')

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """UPDATE resultados SET campeonato_id = %s, equipo_local_id = %s, equipo_visitante_id = %s,
                   marcador_local = %s, marcador_visitante = %s, fecha = %s
                   WHERE id = %s""",
                (campeonato_id, equipo_local_id, equipo_visitante_id, marcador_local, marcador_visitante, fecha, id),
            )
    return redirect('/admin/resultados')


@admin_bp.route('/resultados/<int:id>/eliminar', methods=['POST'])
def resultados_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM resultados WHERE id = %s', (id,))
    return redirect('/admin/resultados')
