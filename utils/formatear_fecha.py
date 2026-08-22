def formatear_fecha(fecha):
    """Igual que new Date(fecha).toLocaleDateString('es-CO') en JS: d/m/aaaa sin ceros a la izquierda."""
    if not fecha:
        return ''
    return f'{fecha.day}/{fecha.month}/{fecha.year}'
