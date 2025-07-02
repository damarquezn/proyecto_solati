import os
from .s3_client import S3ApiClient
from .config import RUTA_SFTP, API_BASE_URL, API_KEY
from .validar import validar_nomenclatura

def subir_archivo_individual(archivo_path, bucket_name, s3_key=None):
    """Sube un archivo individual a S3"""
    cliente = S3ApiClient(API_BASE_URL, API_KEY)
    
    if not os.path.exists(archivo_path):
        return {"estado": "error", "mensaje": "Archivo no encontrado"}
    
    if s3_key is None:
        s3_key = os.path.basename(archivo_path)
    
    try:
        resultado = cliente.upload_file(
            bucket_name=bucket_name,
            file_path=archivo_path,
            file_name=s3_key
        )
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
        print(f"✗ Error al subir {s3_key}: {error_msg}")
        return {"estado": "error", "mensaje": error_msg}

def subir_carpeta_especifica(nombre_carpeta, bucket_name):
    """Sube todos los archivos de una carpeta específica"""
    cliente = S3ApiClient(API_BASE_URL, API_KEY)
    ruta_carpeta = os.path.join(RUTA_SFTP, nombre_carpeta)
    
    if not os.path.exists(ruta_carpeta):
        return {"estado": "error", "mensaje": "Carpeta no encontrada"}
    
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

def subir_todas_las_carpetas(bucket_name):
    """Sube todos los archivos de todas las carpetas en RUTA_SFTP"""
    if not os.path.exists(RUTA_SFTP):
        return {"estado": "error", "mensaje": "Ruta SFTP no encontrada"}
    
    resultados = {}
    carpetas = [d for d in os.listdir(RUTA_SFTP) if os.path.isdir(os.path.join(RUTA_SFTP, d))]
    
    for carpeta in carpetas:
        print(f"Procesando carpeta: {carpeta}")
        resultado_carpeta = subir_carpeta_especifica(carpeta, bucket_name)
        resultados[carpeta] = resultado_carpeta
    
    return resultados

def subir_audios_a_s3(diccionario_audios, bucket_name):
    """Sube archivos específicos organizados por carpeta (reutiliza lógica existente)"""
    resultados = {}
    
    for nombre_carpeta in diccionario_audios.keys():
        print(f"Procesando carpeta: {nombre_carpeta}")
        resultado_carpeta = subir_carpeta_especifica(nombre_carpeta, bucket_name)
        resultados[nombre_carpeta] = resultado_carpeta.get("archivos", [])
    
    return resultados