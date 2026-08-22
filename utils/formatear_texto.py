import re


def _escapar_html(texto):
    return (
        texto.replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
    )


def formatear_texto(texto):
    """Convierte *texto* o **texto** en negrilla, como en WhatsApp.
    El texto se escapa primero para que no se pueda inyectar HTML."""
    if not texto:
        return ''
    escapado = _escapar_html(texto)
    escapado = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', escapado)
    escapado = re.sub(r'\*(.+?)\*', r'<strong>\1</strong>', escapado)
    return escapado
