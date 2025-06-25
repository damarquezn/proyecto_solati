import datetime

def convertir_timestamp_a_humano(timestamp_unix):
    """Convierte timestamp Unix a formato: YYYY_MM_DD_HH:MM:SS"""
    try:
        dt = datetime.datetime.fromtimestamp(int(timestamp_unix))
        return dt.strftime("%Y_%m_%d__%H:%M:%S")
    except (ValueError, OSError):
        return "fecha_invalida"