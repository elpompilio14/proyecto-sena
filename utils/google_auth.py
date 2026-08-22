import os
from urllib.parse import urlencode
import requests


def url_autorizacion_google(state):
    params = {
        'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
        'redirect_uri': os.environ.get('GOOGLE_CALLBACK_URL'),
        'response_type': 'code',
        'scope': 'openid email profile',
        'prompt': 'select_account',
        'state': state,
    }
    return f'https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}'


def obtener_perfil_google(code):
    respuesta_token = requests.post('https://oauth2.googleapis.com/token', data={
        'code': code,
        'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
        'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
        'redirect_uri': os.environ.get('GOOGLE_CALLBACK_URL'),
        'grant_type': 'authorization_code',
    })
    datos_token = respuesta_token.json()
    if not respuesta_token.ok:
        raise Exception(datos_token.get('error_description', 'No se pudo validar con Google'))

    respuesta_perfil = requests.get(
        'https://www.googleapis.com/oauth2/v2/userinfo',
        headers={'Authorization': f"Bearer {datos_token['access_token']}"},
    )
    perfil = respuesta_perfil.json()
    if not respuesta_perfil.ok:
        raise Exception('No se pudo obtener el perfil de Google')

    return perfil  # { id, email, given_name, family_name, name, picture, verified_email }
