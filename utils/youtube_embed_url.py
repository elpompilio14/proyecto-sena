import re

PATRONES = [
    r'youtu\.be/([a-zA-Z0-9_-]{11})',
    r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
    r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
    r'youtube\.com/shorts/([a-zA-Z0-9_-]{11})',
]


def youtube_embed_url(url):
    """Convierte un link normal de YouTube (watch, youtu.be, shorts) en su URL de incrustar (embed)."""
    if not url:
        return None
    for patron in PATRONES:
        coincidencia = re.search(patron, url)
        if coincidencia:
            return f'https://www.youtube.com/embed/{coincidencia.group(1)}'
    return None
