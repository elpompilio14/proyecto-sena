import re


def whatsapp_numero(numero):
    """Limpia el numero de WhatsApp guardado en admin (puede tener espacios, guiones,
    parentesis o venir sin el indicativo de pais) para que el link a wa.me funcione."""
    if not numero:
        return None
    solo_digitos = re.sub(r'\D', '', numero)
    if len(solo_digitos) == 10:
        return '57' + solo_digitos  # celular colombiano sin indicativo
    return solo_digitos
