import requests
from .s3_client import S3ApiClient
from .config import API_BASE_URL, API_KEY

def listar_buckets():
    """
    Lista todos los buckets disponibles en S3
    
    Returns:
        list: Lista de nombres de buckets
    """
    cliente = S3ApiClient(API_BASE_URL, API_KEY)
    return cliente.list_buckets()

def listar_objetos_bucket(bucket_name):
    """
    Lista todos los objetos en un bucket específico
    
    Args:
        bucket_name (str): Nombre del bucket
        
    Returns:
        list: Lista de objetos en el bucket
    """
    cliente = S3ApiClient(API_BASE_URL, API_KEY)
    url = f"{API_BASE_URL}/s3/buckets/{bucket_name}/objects"
    response = requests.get(url, headers=cliente.headers)
    return response.json()