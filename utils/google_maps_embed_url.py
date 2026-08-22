from urllib.parse import quote


def google_maps_embed_url(direccion):
    """Genera un link para incrustar Google Maps a partir de una direccion, sin necesitar API key."""
    if not direccion:
        return None
    return f'https://www.google.com/maps?q={quote(direccion)}&output=embed'
