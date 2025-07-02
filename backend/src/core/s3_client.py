import requests
import base64
import os

class S3ApiClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {"API-Key": api_key}
        self.json_headers = {**self.headers, "Content-Type": "application/json"}
    
    def list_buckets(self):
        """Obtiene la lista de todos los buckets disponibles"""
        url = f"{self.base_url}/s3/buckets"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def upload_file(self, bucket_name, file_path, file_name=None):
        """Sube un archivo a un bucket específico"""
        if file_name is None:
            file_name = os.path.basename(file_path)
        
        url = f"{self.base_url}/s3/buckets/{bucket_name}/objects"
        
        with open(file_path, "rb") as file:
            file_content = base64.b64encode(file.read()).decode('utf-8')
        
        data = {
            "file_content": file_content,
            "file_name": file_name
        }
        
        response = requests.post(url, headers=self.json_headers, json=data)
        
        # Verificar el código de estado HTTP
        if response.status_code != 200:
            raise Exception(f"Error HTTP {response.status_code}: {response.text}")
            
        return response.json()
    
    def delete_file(self, bucket_name, object_key):
        """Elimina un archivo de un bucket específico
        
        Args:
            bucket_name (str): Nombre del bucket
            object_key (str): Clave del objeto a eliminar
            
        Returns:
            dict: Resultado de la operación
        """
        url = f"{self.base_url}/s3/buckets/{bucket_name}/objects/"
        params = {"object_key": object_key}
        
        response = requests.delete(url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Error HTTP {response.status_code}: {response.text}")
        
        return response.json()