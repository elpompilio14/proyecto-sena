import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def _enviar(destinatario, asunto, html):
    usuario = os.environ.get('GMAIL_USER')
    clave_app = os.environ.get('GMAIL_APP_PASSWORD')

    mensaje = MIMEMultipart('alternative')
    mensaje['From'] = f'IED Talento Humano <{usuario}>'
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(html, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
        servidor.starttls()
        servidor.login(usuario, clave_app)
        servidor.sendmail(usuario, destinatario, mensaje.as_string())


def enviar_codigo_verificacion(destinatario, nombre, codigo):
    html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;">
            <h2 style="color: #073d82;">Hola, {nombre}</h2>
            <p>Usa este código para confirmar tu correo en la página del colegio:</p>
            <p style="font-size: 32px; font-weight: bold; letter-spacing: 6px; color: #0a5ec4; text-align: center; padding: 16px; background: #e6f1ff; border-radius: 10px;">{codigo}</p>
            <p>Este código vence en 15 minutos. Si no creaste esta cuenta, ignora este mensaje.</p>
        </div>
    """
    _enviar(destinatario, 'Verifica tu correo - IED Talento Humano', html)


def enviar_codigo_recuperacion(destinatario, nombre, codigo):
    html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;">
            <h2 style="color: #073d82;">Hola, {nombre}</h2>
            <p>Recibimos una solicitud para restablecer tu contraseña. Usa este código para continuar:</p>
            <p style="font-size: 32px; font-weight: bold; letter-spacing: 6px; color: #0a5ec4; text-align: center; padding: 16px; background: #e6f1ff; border-radius: 10px;">{codigo}</p>
            <p>Este código vence en 15 minutos. Si tú no pediste esto, ignora este mensaje y tu contraseña seguirá igual.</p>
        </div>
    """
    _enviar(destinatario, 'Restablece tu contraseña - IED Talento Humano', html)
