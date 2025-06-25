def obtener_formato(archivo):
    if '.' in archivo:
        return archivo.rsplit('.', 1)[1].lower()
    return "desconocido"