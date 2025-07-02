from mutagen import File as MutagenFile

def extraer_duracion_segundos(ruta_archivo):
    try:
        audio = MutagenFile(ruta_archivo)
        if audio is not None and hasattr(audio.info, 'length'):
            return round(audio.info.length, 2)
    except Exception as e:
        print(f"No se pudo leer duración para {ruta_archivo}: {e}")
    return 0 