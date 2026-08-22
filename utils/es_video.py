EXTENSIONES_VIDEO = ['.mp4', '.webm', '.mov', '.ogg']


def es_video(url):
    if not url:
        return False
    minuscula = url.lower()
    return any(minuscula.endswith(ext) for ext in EXTENSIONES_VIDEO)
