import os
import datetime
from mutagen import File as MutagenFile

RUTA_SFTP = os.path.expanduser('~/nuevo_proyecto/proyecto_solati/simulador-SFTP')

def extraer_duracion_segundos(ruta_archivo):
    try:
        audio = MutagenFile(ruta_archivo)
        if audio is not None and hasattr(audio.info, 'length'):
            return round(audio.info.length, 2)
    except Exception as e:
        print(f"[Error] No se pudo leer duración para {ruta_archivo}: {e}")
    return 0 


def validar_nomenclatura(archivo):
    if '-' not in archivo or '.' not in archivo:
        return False
    
    nombre_sin_ext = archivo.rsplit('.', 1)[0]
    partes = nombre_sin_ext.split('-')
    
    # Debe tener exactamente 4 partes: id_casa-identificacion-telefono-timestamp
    if len(partes) != 4:
        return False
    
    id_casa, identificacion_deudor, telefono, timestamp = partes

    if len(telefono) != 10:
        return False
    
    # Validar que timestamp sea numérico y tenga al menos 10 dígitos (Unix timestamp)
    if not timestamp.isdigit() or len(timestamp) < 10:
        return False
    
    # Validar que identificación y teléfono sean numéricos
    if not identificacion_deudor.isdigit() or not telefono.isdigit():
        return False
    
    return True

def convertir_timestamp_a_humano(timestamp_unix):
    """Convierte timestamp Unix a formato: YYYY_MM_DD_HH:MM:SS"""
    try:
        dt = datetime.datetime.fromtimestamp(int(timestamp_unix))
        return dt.strftime("%Y_%m_%d__%H:%M:%S")
    except (ValueError, OSError):
        return "fecha_invalida"

def recorrer_archivos(ruta_SFTP):
    audios_por_carpeta = {}
    for nombre_carpeta in sorted(os.listdir(ruta_SFTP)):
        ruta_carpeta = os.path.join(ruta_SFTP, nombre_carpeta)
        if os.path.isdir(ruta_carpeta):
            audios = sorted([
                archivo for archivo in os.listdir(ruta_carpeta)
                if archivo.lower().endswith(('.wav', '.mp3', '.aac', '.ogg'))
                and validar_nomenclatura(archivo)
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
                # Extraer timestamp del nombre del archivo
                nombre_sin_ext = audio.rsplit('.', 1)[0]
                partes = nombre_sin_ext.split('-')
                if len(partes) == 4:
                    timestamp = partes[-1]
                    fecha_humana = convertir_timestamp_a_humano(timestamp)
                    ruta_completa = os.path.join(RUTA_SFTP, nombre_carpeta, audio)
                    duracion = extraer_duracion_segundos(ruta_completa)
                    print(f"  - {audio} ({fecha_humana}) \n    - Duracion: {duracion} segundos \n    - ID Casa: {partes[0]} \n    - Identificación Deudor: {partes[1]} \n    - Numero Telefono: {partes[2]} \n    - Unixtime: {timestamp} \n    - Fecha: {fecha_humana}")
                else:
                    print(f"  - {audio}")
        else:
            print("  (sin archivos)")


if __name__ == "__main__":
    audios_por_carpeta = recorrer_archivos(RUTA_SFTP)
    imprimir_resumen_audios(audios_por_carpeta)

