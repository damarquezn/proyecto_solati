import os

RUTA_SFTP = os.path.expanduser('~/nuevo_proyecto/proyecto_solati/simulador-SFTP')

def validar_nomenclatura(archivo, nombre_carpeta):
    if '-' not in archivo or '.' not in archivo:
        return False
    
    nombre_sin_ext = archivo.rsplit('.', 1)[0]
    partes = nombre_sin_ext.split('-')
    if len(partes) < 2:
        return False
    
    timestamp = partes[-1]
    id_casa = '-'.join(partes[:-1])
    
    return id_casa == nombre_carpeta and timestamp.isdigit() and len(timestamp) >= 10

def recorrer_archivos(ruta_SFTP):
    audios_por_carpeta = {}
    for nombre_carpeta in sorted(os.listdir(ruta_SFTP)):
        ruta_SFTP = os.path.join(ruta_SFTP, nombre_carpeta)
        if os.path.isdir(ruta_SFTP):
            audios = sorted([
                archivo for archivo in os.listdir(ruta_SFTP)
                if archivo.lower().endswith(('.mp3', '.wav', '.aac', '.ogg'))
                and validar_nomenclatura(archivo, nombre_carpeta)
            ])
            audios_por_carpeta[nombre_carpeta] = audios
    return audios_por_carpeta

def imprimir_resumen_audios(diccionario_audios):
    print("Lista de archivos por carpeta:")
    print()
    for nombre_carpeta, audios in diccionario_audios.items():
        print(f"Carpeta: {nombre_carpeta}")
        if audios:
            for audio in audios:
                print(f"  - {audio}")
        else:
            print("  (sin archivos)")


if __name__ == "__main__":
    audios_por_carpeta = recorrer_archivos(RUTA_SFTP)
    imprimir_resumen_audios(audios_por_carpeta)

