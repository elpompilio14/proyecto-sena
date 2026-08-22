from flask import render_template, request, redirect, abort
from . import admin_bp
from db import obtener_conexion


@admin_bp.route('/mejores-puestos')
def mejores_puestos_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute("""
                SELECT mejores_puestos.*, estudiantes.nombres, estudiantes.apellidos, grados.nombre AS grado_nombre
                FROM mejores_puestos
                JOIN estudiantes ON estudiantes.id = mejores_puestos.estudiante_id
                JOIN grados ON grados.id = mejores_puestos.grado_id
                ORDER BY grados.nivel, mejores_puestos.periodo DESC, mejores_puestos.puesto
            """)
            puestos = cur.fetchall()
            cur.execute('SELECT id, nombres, apellidos FROM estudiantes ORDER BY apellidos, nombres')
            estudiantes = cur.fetchall()
            cur.execute('SELECT * FROM grados ORDER BY nivel, nombre')
            grados = cur.fetchall()

    return render_template(
        'admin/mejores_puestos.html', titulo='Admin · Puestos de honor', puestos=puestos, estudiantes=estudiantes, grados=grados,
    )


@admin_bp.route('/mejores-puestos', methods=['POST'])
def mejores_puestos_crear():
    estudiante_id = request.form.get('estudiante_id')
    grado_id = request.form.get('grado_id')
    periodo = request.form.get('periodo')
    puesto = request.form.get('puesto')
    promedio = request.form.get('promedio') or None

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """INSERT INTO mejores_puestos (estudiante_id, grado_id, periodo, puesto, promedio)
                   VALUES (%s, %s, %s, %s, %s)""",
                (estudiante_id, grado_id, periodo, puesto, promedio),
            )
    return redirect('/admin/mejores-puestos')


@admin_bp.route('/mejores-puestos/<int:id>/editar')
def mejores_puestos_editar_form(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM mejores_puestos WHERE id = %s', (id,))
            puesto = cur.fetchone()
            if not puesto:
                abort(404)
            cur.execute('SELECT id, nombres, apellidos FROM estudiantes ORDER BY apellidos, nombres')
            estudiantes = cur.fetchall()
            cur.execute('SELECT * FROM grados ORDER BY nivel, nombre')
            grados = cur.fetchall()

    return render_template(
        'admin/mejores_puestos_editar.html', titulo='Admin · Editar puesto de honor', puesto=puesto, estudiantes=estudiantes, grados=grados,
    )


@admin_bp.route('/mejores-puestos/<int:id>/editar', methods=['POST'])
def mejores_puestos_editar(id):
    estudiante_id = request.form.get('estudiante_id')
    grado_id = request.form.get('grado_id')
    periodo = request.form.get('periodo')
    puesto = request.form.get('puesto')
    promedio = request.form.get('promedio') or None

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                """UPDATE mejores_puestos SET estudiante_id = %s, grado_id = %s, periodo = %s, puesto = %s, promedio = %s
                   WHERE id = %s""",
                (estudiante_id, grado_id, periodo, puesto, promedio, id),
            )
    return redirect('/admin/mejores-puestos')


@admin_bp.route('/mejores-puestos/<int:id>/eliminar', methods=['POST'])
def mejores_puestos_eliminar(id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('DELETE FROM mejores_puestos WHERE id = %s', (id,))
    return redirect('/admin/mejores-puestos')
