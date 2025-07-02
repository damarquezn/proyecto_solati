from .s3_client import S3ApiClient
from .config import API_BASE_URL, API_KEY

def borrar_archivo_s3(bucket_name, object_key):
    """
    Elimina un archivo específico de un bucket S3
    
    Args:
        bucket_name (str): Nombre del bucket
        object_key (str): Clave del objeto a eliminar (ej: "carpeta/archivo.mp3")
    
    Returns:
        dict: Resultado de la operación
    """
    cliente = S3ApiClient(API_BASE_URL, API_KEY)
    
    try:
        resultado = cliente.delete_file(bucket_name, object_key)
        print(f"  ✓ Eliminado: {object_key}")
        return {
            "archivo": object_key,
            "estado": "eliminado",
            "mensaje": resultado.get("message", "Archivo eliminado exitosamente")
        }
    except Exception as e:
        error_msg = str(e)
        print(f"  ✗ Error al eliminar {object_key}: {error_msg}")
        return {
            "archivo": object_key,
            "estado": "error",
            "mensaje": error_msg
        }

def borrar_multiples_archivos_s3(bucket_name, object_keys):
    """
    Elimina múltiples archivos de un bucket S3
    
    Args:
        bucket_name (str): Nombre del bucket
        object_keys (list): Lista de claves de objetos a eliminar
    
    Returns:
        list: Lista con resultados de cada eliminación
    """
    resultados = []
    
    for object_key in object_keys:
        resultado = borrar_archivo_s3(bucket_name, object_key)
        resultados.append(resultado)
    
    return resultados