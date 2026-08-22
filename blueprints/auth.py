import os
import secrets
from datetime import datetime, timedelta

import bcrypt
from flask import Blueprint, render_template, request, redirect, session, url_for

from db import obtener_conexion
from utils.generar_codigo import generar_codigo
from mailer import enviar_codigo_verificacion, enviar_codigo_recuperacion
from utils.google_auth import url_autorizacion_google, obtener_perfil_google

auth_bp = Blueprint('auth', __name__)

MINUTOS_EXPIRACION_CODIGO = 15


def _hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def _verificar_password(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


@auth_bp.route('/registro', methods=['GET'])
def registro_form():
    return render_template('auth.html', titulo='Crear cuenta', tabActiva='registro', errorLogin=None, errorRegistro=None)


@auth_bp.route('/registro', methods=['POST'])
def registro():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirmar = request.form.get('password_confirmar')

    if not nombre or not apellido or not email or not password or not password_confirmar:
        return render_template(
            'auth.html', titulo='Crear cuenta', tabActiva='registro', errorLogin=None,
            errorRegistro='Todos los campos son obligatorios',
        ), 400

    if password != password_confirmar:
        return render_template(
            'auth.html', titulo='Crear cuenta', tabActiva='registro', errorLogin=None,
            errorRegistro='Las contraseñas no coinciden',
        ), 400

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT id FROM usuarios WHERE email = %s', (email,))
            if cur.fetchone():
                return render_template(
                    'auth.html', titulo='Crear cuenta', tabActiva='registro', errorLogin=None,
                    errorRegistro='Ese correo ya está registrado',
                ), 400

            password_hash = _hash_password(password)
            codigo = generar_codigo()
            expira = datetime.now() + timedelta(minutes=MINUTOS_EXPIRACION_CODIGO)

            cur.execute(
                """INSERT INTO usuarios (nombre, apellido, email, password_hash, rol, verificado, codigo_verificacion, codigo_expira)
                   VALUES (%s, %s, %s, %s, 'usuario', false, %s, %s)""",
                (nombre, apellido, email, password_hash, codigo, expira),
            )

    try:
        enviar_codigo_verificacion(email, nombre, codigo)
    except Exception as err:
        print('No se pudo enviar el correo de verificación:', err)

    return redirect(f'/verificar-correo?email={email}')


@auth_bp.route('/verificar-correo', methods=['GET'])
def verificar_form():
    return render_template('verificar_correo.html', titulo='Verificar correo', email=request.args.get('email', ''), error=None)


@auth_bp.route('/verificar-correo', methods=['POST'])
def verificar():
    email = request.form.get('email')
    codigo = request.form.get('codigo')

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
            usuario = cur.fetchone()

            if not usuario:
                return render_template('verificar_correo.html', titulo='Verificar correo', email=email, error='No encontramos esa cuenta'), 400

            if usuario['verificado']:
                session['usuario'] = {'id': usuario['id'], 'nombre': usuario['nombre'], 'rol': usuario['rol']}
                return redirect('/')

            expirado = not usuario['codigo_expira'] or usuario['codigo_expira'] < datetime.now()
            if expirado:
                return render_template(
                    'verificar_correo.html', titulo='Verificar correo', email=email, error='El código venció, pide uno nuevo',
                ), 400

            if usuario['codigo_verificacion'] != codigo:
                return render_template('verificar_correo.html', titulo='Verificar correo', email=email, error='Código incorrecto'), 400

            cur.execute(
                'UPDATE usuarios SET verificado = true, codigo_verificacion = null, codigo_expira = null WHERE id = %s',
                (usuario['id'],),
            )

    session['usuario'] = {'id': usuario['id'], 'nombre': usuario['nombre'], 'rol': usuario['rol']}
    return redirect('/')


@auth_bp.route('/verificar-correo/reenviar', methods=['POST'])
def reenviar_codigo():
    email = request.form.get('email')

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
            usuario = cur.fetchone()

            if usuario and not usuario['verificado']:
                codigo = generar_codigo()
                expira = datetime.now() + timedelta(minutes=MINUTOS_EXPIRACION_CODIGO)
                cur.execute('UPDATE usuarios SET codigo_verificacion = %s, codigo_expira = %s WHERE id = %s', (codigo, expira, usuario['id']))
                try:
                    enviar_codigo_verificacion(usuario['email'], usuario['nombre'], codigo)
                except Exception as err:
                    print('No se pudo reenviar el correo de verificación:', err)

    return render_template('verificar_correo.html', titulo='Verificar correo', email=email, error=None, reenviado=True)


@auth_bp.route('/login', methods=['GET'])
def login_form():
    return render_template(
        'auth.html', titulo='Iniciar sesión', tabActiva='login', errorLogin=None, errorRegistro=None,
        exitoLogin='Tu contraseña fue actualizada. Ya puedes iniciar sesión.' if request.args.get('restablecida') else None,
    )


@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
            usuario = cur.fetchone()

    if not usuario or not usuario['password_hash']:
        return render_template(
            'auth.html', titulo='Iniciar sesión', tabActiva='login',
            errorLogin='Correo o contraseña incorrectos' if not usuario else 'Esta cuenta inicia sesión con Google, usa ese botón',
            errorRegistro=None,
        ), 401

    if not _verificar_password(password, usuario['password_hash']):
        return render_template(
            'auth.html', titulo='Iniciar sesión', tabActiva='login',
            errorLogin='Correo o contraseña incorrectos', errorRegistro=None,
        ), 401

    if not usuario['verificado']:
        return redirect(f"/verificar-correo?email={usuario['email']}")

    session['usuario'] = {'id': usuario['id'], 'nombre': usuario['nombre'], 'rol': usuario['rol']}
    return redirect('/admin' if usuario['rol'] == 'admin' else '/')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/login')


@auth_bp.route('/recuperar-contrasena', methods=['GET'])
def recuperar_form():
    return render_template('recuperar_contrasena.html', titulo='Recuperar contraseña', error=None)


@auth_bp.route('/recuperar-contrasena', methods=['POST'])
def recuperar():
    email = request.form.get('email')

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
            usuario = cur.fetchone()

            if not usuario:
                return render_template(
                    'recuperar_contrasena.html', titulo='Recuperar contraseña',
                    error='No encontramos una cuenta con ese correo',
                ), 400

            if not usuario['password_hash']:
                return render_template(
                    'recuperar_contrasena.html', titulo='Recuperar contraseña',
                    error='Esta cuenta inicia sesión con Google, no tiene contraseña que restablecer',
                ), 400

            codigo = generar_codigo()
            expira = datetime.now() + timedelta(minutes=MINUTOS_EXPIRACION_CODIGO)
            cur.execute('UPDATE usuarios SET codigo_verificacion = %s, codigo_expira = %s WHERE id = %s', (codigo, expira, usuario['id']))

    try:
        enviar_codigo_recuperacion(usuario['email'], usuario['nombre'], codigo)
    except Exception as err:
        print('No se pudo enviar el correo de recuperación:', err)

    return redirect(f'/recuperar-contrasena/verificar?email={email}')


@auth_bp.route('/recuperar-contrasena/verificar', methods=['GET'])
def recuperar_verificar_form():
    return render_template(
        'recuperar_contrasena_verificar.html', titulo='Restablecer contraseña',
        email=request.args.get('email', ''), error=None,
    )


@auth_bp.route('/recuperar-contrasena/verificar', methods=['POST'])
def recuperar_verificar():
    email = request.form.get('email')
    codigo = request.form.get('codigo')
    password = request.form.get('password')
    password_confirmar = request.form.get('password_confirmar')

    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
            usuario = cur.fetchone()

            if not usuario:
                return render_template('recuperar_contrasena_verificar.html', titulo='Restablecer contraseña', email=email, error='No encontramos esa cuenta'), 400

            expirado = not usuario['codigo_expira'] or usuario['codigo_expira'] < datetime.now()
            if expirado:
                return render_template(
                    'recuperar_contrasena_verificar.html', titulo='Restablecer contraseña', email=email,
                    error='El código venció, pide uno nuevo',
                ), 400

            if usuario['codigo_verificacion'] != codigo:
                return render_template(
                    'recuperar_contrasena_verificar.html', titulo='Restablecer contraseña', email=email, error='Código incorrecto',
                ), 400

            if not password or len(password) < 6:
                return render_template(
                    'recuperar_contrasena_verificar.html', titulo='Restablecer contraseña', email=email,
                    error='La contraseña debe tener al menos 6 caracteres',
                ), 400

            if password != password_confirmar:
                return render_template(
                    'recuperar_contrasena_verificar.html', titulo='Restablecer contraseña', email=email,
                    error='Las contraseñas no coinciden',
                ), 400

            password_hash = _hash_password(password)
            cur.execute(
                'UPDATE usuarios SET password_hash = %s, verificado = true, codigo_verificacion = null, codigo_expira = null WHERE id = %s',
                (password_hash, usuario['id']),
            )

    return redirect('/login?restablecida=1')


@auth_bp.route('/auth/google')
def iniciar_google():
    state = secrets.token_hex(16)
    session['googleState'] = state
    return redirect(url_autorizacion_google(state))


@auth_bp.route('/auth/google/callback')
def callback_google():
    code = request.args.get('code')
    state = request.args.get('state')

    if not code or not state or state != session.get('googleState'):
        return redirect('/login')

    try:
        perfil = obtener_perfil_google(code)

        with obtener_conexion() as conexion:
            with conexion.cursor() as cur:
                cur.execute('SELECT * FROM usuarios WHERE google_id = %s', (perfil['id'],))
                usuario = cur.fetchone()

                if not usuario:
                    cur.execute('SELECT * FROM usuarios WHERE email = %s', (perfil['email'],))
                    usuario = cur.fetchone()

                    if usuario:
                        cur.execute('UPDATE usuarios SET google_id = %s, verificado = true WHERE id = %s', (perfil['id'], usuario['id']))
                    else:
                        cur.execute(
                            """INSERT INTO usuarios (nombre, apellido, email, password_hash, rol, verificado, google_id)
                               VALUES (%s, %s, %s, NULL, 'usuario', true, %s)
                               RETURNING id, nombre, rol""",
                            (perfil.get('given_name') or perfil.get('name') or 'Usuario', perfil.get('family_name') or '', perfil['email'], perfil['id']),
                        )
                        usuario = cur.fetchone()

        session['usuario'] = {'id': usuario['id'], 'nombre': usuario['nombre'], 'rol': usuario['rol']}
        return redirect('/admin' if usuario['rol'] == 'admin' else '/')
    except Exception as err:
        print('Error en login con Google:', err)
        return redirect('/login')
