import os
from .validar import validar_nomenclatura

def recorrer_archivos(ruta):
    audios_por_carpeta = {}
    for nombre_carpeta in sorted(os.listdir(ruta)):
        ruta_carpeta = os.path.join(ruta, nombre_carpeta)
        if os.path.isdir(ruta_carpeta):
            audios = sorted([
                archivo for archivo in os.listdir(ruta_carpeta)
                if archivo.lower().endswith(('.wav', '.mp3', '.aac', '.ogg'))
                and validar_nomenclatura(archivo)
            ])
            audios_por_carpeta[nombre_carpeta] = audios
    return audios_por_carpeta