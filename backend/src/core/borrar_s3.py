import logging
from .s3_client import S3ApiClient
from .config import API_BASE_URL, API_KEY
from .listar_s3 import listar_objetos_bucket

logger = logging.getLogger(__name__)

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
    
    logger.info(f"Eliminando archivo: {object_key} del bucket: {bucket_name}")
    
    try:
        resultado = cliente.delete_file(bucket_name, object_key)
        logger.info(f"Archivo eliminado exitosamente: {object_key}")
        print(f"  ✓ Eliminado: {object_key}")
        return {
            "archivo": object_key,
            "estado": "eliminado",
            "mensaje": resultado.get("message", "Archivo eliminado exitosamente")
        }
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error al eliminar archivo {object_key}: {error_msg}")
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
    logger.info(f"Eliminando {len(object_keys)} archivos del bucket: {bucket_name}")
    
    resultados = []
    
    for object_key in object_keys:
        resultado = borrar_archivo_s3(bucket_name, object_key)
        resultados.append(resultado)
    
    exitosos = sum(1 for r in resultados if r['estado'] == 'eliminado')
    errores = len(resultados) - exitosos
    logger.info(f"Eliminación múltiple completada: {exitosos} exitosos, {errores} errores")
    
    return resultados

def borrar_todo_bucket(bucket_name):
    """
    Elimina todos los objetos de un bucket S3
    
    Args:
        bucket_name (str): Nombre del bucket
    
    Returns:
        dict: Resultado de la operación con estadísticas
    """
    logger.info(f"Iniciando vaciado completo del bucket: {bucket_name}")
    
    try:
        # Listar todos los objetos del bucket
        objetos = listar_objetos_bucket(bucket_name)
        
        if not objetos:
            logger.info(f"Bucket {bucket_name} ya está vacío")
            return {
                'estado': 'vacio',
                'mensaje': 'El bucket está vacío',
                'total_objetos': 0,
                'eliminados': 0,
                'errores': 0
            }
        
        logger.info(f"Se encontraron {len(objetos)} objetos para eliminar")
        
        # Extraer las claves de los objetos
        claves = [obj['key'] for obj in objetos]
        
        # Eliminar todos los objetos usando la función existente
        resultados = borrar_multiples_archivos_s3(bucket_name, claves)
        
        eliminados = sum(1 for r in resultados if r['estado'] == 'eliminado')
        errores = len(resultados) - eliminados
        
        logger.info(f"Vaciado completado: {eliminados} eliminados, {errores} errores")
        
        return {
            'estado': 'completado',
            'mensaje': f'Proceso completado: {eliminados} eliminados, {errores} errores',
            'total_objetos': len(objetos),
            'eliminados': eliminados,
            'errores': errores,
            'resultados': resultados
        }
        
    except Exception as e:
        logger.error(f"Error al vaciar bucket {bucket_name}: {str(e)}")
        return {
            'estado': 'error',
            'mensaje': f'Error al vaciar el bucket: {str(e)}',
            'total_objetos': 0,
            'eliminados': 0,
            'errores': 1
        }