import os

def obtener_tamano_archivo(ruta_archivo):
    """
    Obtiene el tamaño de un archivo en bytes
    
    Args:
        ruta_archivo (str): Ruta completa al archivo
        
    Returns:
        int: Tamaño del archivo en bytes, 0 si hay error
    """
    try:
        return os.path.getsize(ruta_archivo)
    except (OSError, FileNotFoundError) as e:
        print(f"No se pudo obtener el tamaño para {ruta_archivo}: {e}")
        return 0

def formatear_tamano(tamano_bytes):
    """
    Convierte bytes a formato legible (KB, MB, GB)
    
    Args:
        tamano_bytes (int): Tamaño en bytes
        
    Returns:
        str: Tamaño formateado (ej: "2.5 MB")
    """
    if tamano_bytes < 1024:
        return f"{tamano_bytes} B"
    elif tamano_bytes < 1024**2:
        return f"{tamano_bytes/1024:.1f} KB"
    elif tamano_bytes < 1024**3:
        return f"{tamano_bytes/(1024**2):.1f} MB"
    else:
        return f"{tamano_bytes/(1024**3):.1f} GB"