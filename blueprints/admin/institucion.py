from flask import render_template, request, redirect
from . import admin_bp
from db import obtener_conexion
from uploads import guardar_archivo, TIPOS_DOCUMENTO


@admin_bp.route('/institucion')
def institucion_index():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM institucion_info ORDER BY id LIMIT 1')
            info = cur.fetchone()
    return render_template('admin/institucion.html', titulo='Admin · Institución', info=info)


@admin_bp.route('/institucion', methods=['POST'])
def institucion_actualizar():
    f = request.form

    escudo_url = guardar_archivo(request.files.get('escudo')) or (f.get('escudo_url_actual') or None)
    bandera_url = guardar_archivo(request.files.get('bandera')) or (f.get('bandera_url_actual') or None)
    fondo_url = guardar_archivo(request.files.get('fondo')) or (f.get('fondo_url_actual') or None)
    logo_url = guardar_archivo(request.files.get('logo')) or (f.get('logo_url_actual') or None)
    instagram_imagen_url = guardar_archivo(request.files.get('instagram_imagen')) or (f.get('instagram_imagen_url_actual') or None)
    facebook_imagen_url = guardar_archivo(request.files.get('facebook_imagen')) or (f.get('facebook_imagen_url_actual') or None)
    plataforma_virtual_logo_url = guardar_archivo(request.files.get('plataforma_virtual_logo')) or (f.get('plataforma_virtual_logo_url_actual') or None)
    manual_convivencia_url = guardar_archivo(request.files.get('manual_convivencia'), tipos_permitidos=TIPOS_DOCUMENTO) or (f.get('manual_convivencia_url_actual') or None)
    manual_convivencia_imagen_url = guardar_archivo(request.files.get('manual_convivencia_imagen')) or (f.get('manual_convivencia_imagen_url_actual') or None)

    valores = (
        f.get('historia'), f.get('mision'), f.get('vision'), f.get('principios'), f.get('valores'),
        f.get('ubicacion_sede1'), f.get('ubicacion_sede2'),
        f.get('telefono') or None, f.get('correo') or None,
        f.get('himno_url') or None, f.get('himno_letra') or None,
        f.get('escudo_texto') or None, escudo_url, f.get('bandera_texto') or None, bandera_url, fondo_url,
        logo_url, f.get('anios_fundacion') or None, f.get('num_estudiantes') or None, f.get('num_profesores') or None,
        f.get('whatsapp_numero') or None, f.get('instagram_url') or None, instagram_imagen_url,
        f.get('facebook_url') or None, facebook_imagen_url,
        f.get('plataforma_virtual_url') or None, plataforma_virtual_logo_url,
        manual_convivencia_url, manual_convivencia_imagen_url,
    )

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT id FROM institucion_info ORDER BY id LIMIT 1')
            existente = cur.fetchone()

            if not existente:
                cur.execute(
                    """INSERT INTO institucion_info
                        (historia, mision, vision, principios, valores, ubicacion_sede1, ubicacion_sede2,
                         telefono, correo, himno_url, himno_letra, escudo_texto, escudo_url, bandera_texto, bandera_url, fondo_url,
                         logo_url, anios_fundacion, num_estudiantes, num_profesores, whatsapp_numero,
                         instagram_url, instagram_imagen_url, facebook_url, facebook_imagen_url,
                         plataforma_virtual_url, plataforma_virtual_logo_url,
                         manual_convivencia_url, manual_convivencia_imagen_url)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    valores,
                )
            else:
                cur.execute(
                    """UPDATE institucion_info
                       SET historia = %s, mision = %s, vision = %s, principios = %s, valores = %s,
                           ubicacion_sede1 = %s, ubicacion_sede2 = %s, telefono = %s, correo = %s,
                           himno_url = %s, himno_letra = %s,
                           escudo_texto = %s, escudo_url = %s, bandera_texto = %s, bandera_url = %s,
                           fondo_url = %s, logo_url = %s, anios_fundacion = %s, num_estudiantes = %s,
                           num_profesores = %s, whatsapp_numero = %s, instagram_url = %s,
                           instagram_imagen_url = %s, facebook_url = %s, facebook_imagen_url = %s,
                           plataforma_virtual_url = %s, plataforma_virtual_logo_url = %s,
                           manual_convivencia_url = %s, manual_convivencia_imagen_url = %s,
                           actualizado_en = NOW()
                       WHERE id = %s""",
                    valores + (existente['id'],),
                )

    return redirect('/admin/institucion')
