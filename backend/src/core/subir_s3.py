import os
import logging
from .s3_client import S3ApiClient
from .config import RUTA_SFTP, API_BASE_URL, API_KEY
from .validar import validar_nomenclatura

logger = logging.getLogger(__name__)

def subir_archivo_individual(archivo_path, bucket_name, s3_key=None):
    """Sube un archivo individual a S3"""
    cliente = S3ApiClient(API_BASE_URL, API_KEY)
    
    if not os.path.exists(archivo_path):
        logger.error(f"Archivo no encontrado: {archivo_path}")
        return {"estado": "error", "mensaje": "Archivo no encontrado"}
    
    if s3_key is None:
        s3_key = os.path.basename(archivo_path)
    
    logger.info(f"Subiendo archivo: {s3_key} al bucket: {bucket_name}")
    
    try:
        resultado = cliente.upload_file(
            bucket_name=bucket_name,
            file_path=archivo_path,
            file_name=s3_key
        )
        logger.info(f"Archivo subido exitosamente: {s3_key}")
        print(f"✓ Subido: {s3_key}")
        return {
            "estado": "subido",
            "archivo": os.path.basename(archivo_path),
            "s3_key": s3_key,
            "url": resultado.get("url", ""),
            "s3_uri": resultado.get("s3_uri", "")
        }
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error al subir archivo {s3_key}: {error_msg}")
        print(f"✗ Error al subir {s3_key}: {error_msg}")
        return {"estado": "error", "mensaje": error_msg}


def subir_carpeta_especifica(nombre_carpeta, bucket_name, ruta_sftp=RUTA_SFTP):
    """Sube todos los archivos de una carpeta específica"""
    cliente = S3ApiClient(API_BASE_URL, API_KEY)
    ruta_carpeta = os.path.join(ruta_sftp, nombre_carpeta)
    
    if not os.path.exists(ruta_carpeta):
        logger.error(f"Carpeta no encontrada: {ruta_carpeta}")
        return {"estado": "error", "mensaje": "Carpeta no encontrada"}
    
    logger.info(f"Subiendo carpeta: {nombre_carpeta} al bucket: {bucket_name}")
    
    resultados = []
    archivos = [f for f in os.listdir(ruta_carpeta) if os.path.isfile(os.path.join(ruta_carpeta, f))]
    
    for archivo in archivos:
        if not validar_nomenclatura(archivo):
            print(f"  ✗ Nomenclatura inválida: {archivo}")
            continue
            
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        s3_key = f"{nombre_carpeta}/{archivo}"
        
        try:
            resultado = cliente.upload_file(
                bucket_name=bucket_name,
                file_path=ruta_completa,
                file_name=s3_key
            )
            resultados.append({
                "archivo": archivo,
                "estado": "subido",
                "s3_key": s3_key,
                "url": resultado.get("url", ""),
                "s3_uri": resultado.get("s3_uri", "")
            })
            print(f"  ✓ Subido: {s3_key}")
        except Exception as e:
            error_msg = str(e)
            print(f"  ✗ Error al subir {s3_key}: {error_msg}")
            resultados.append({
                "archivo": archivo,
                "estado": "error",
                "mensaje": error_msg
            })
    
    return {"carpeta": nombre_carpeta, "archivos": resultados}


def subir_todas_las_carpetas(ruta_sftp=RUTA_SFTP, bucket_name=None):
    """Sube todos los archivos de todas las carpetas en ruta_sftp"""
    if not os.path.exists(ruta_sftp):
        logger.error(f"Ruta SFTP no encontrada: {ruta_sftp}")
        return {"estado": "error", "mensaje": "Ruta SFTP no encontrada"}
    
    logger.info(f"Iniciando subida masiva desde: {ruta_sftp} al bucket: {bucket_name}")
    
    resultados = {}
    carpetas = [d for d in os.listdir(ruta_sftp) if os.path.isdir(os.path.join(ruta_sftp, d))]
    
    logger.info(f"Se encontraron {len(carpetas)} carpetas para procesar")
    
    for carpeta in carpetas:
        logger.info(f"Procesando carpeta: {carpeta}")
        print(f"Procesando carpeta: {carpeta}")
        resultado_carpeta = subir_carpeta_especifica(carpeta, bucket_name, ruta_sftp=ruta_sftp)
        resultados[carpeta] = resultado_carpeta
    
    logger.info(f"Subida masiva completada para {len(carpetas)} carpetas")
    return resultados


def subir_audios_a_s3(diccionario_audios, bucket_name, ruta_sftp=RUTA_SFTP):
    """Sube archivos específicos organizados por carpeta (reutiliza lógica existente)"""
    resultados = {}
    
    for nombre_carpeta in diccionario_audios.keys():
        print(f"Procesando carpeta: {nombre_carpeta}")
        resultado_carpeta = subir_carpeta_especifica(nombre_carpeta, bucket_name, ruta_sftp=ruta_sftp)
        resultados[nombre_carpeta] = resultado_carpeta.get("archivos", [])
    
    return resultados
