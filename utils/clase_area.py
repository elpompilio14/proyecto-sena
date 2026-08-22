def clase_area(area):
    if area == 'Ciencias':
        return 'docente-tag-ciencias'
    if area == 'Humanidades':
        return 'docente-tag-humanidades'
    if area == 'Tecnología':
        return 'docente-tag-tecnologia'
    if area == 'Artes y Ed. Física':
        return 'docente-tag-artes'
    return 'docente-tag-otro'
