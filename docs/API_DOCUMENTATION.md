# API de Gestión de Archivos S3

Esta API permite gestionar archivos en Amazon S3 a través de endpoints REST.

## URL Base

```
https://0s5qqr11v3.execute-api.us-east-1.amazonaws.com/Prod
```

## Autenticación

La mayoría de los endpoints requieren autenticación mediante una API Key. Esta debe enviarse en el header `API-Key`.

```
API-Key: test-api-key-123
```

## Endpoints

### Listar Buckets

Obtiene la lista de todos los buckets S3 disponibles.

**Método:** GET  
**Ruta:** `/s3/buckets`  

**Ejemplo de respuesta:**
```json
[
  {"name": "bucket-1"},
  {"name": "bucket-2"}
]
```

**Ejemplo en Python:**
```python
import requests

url = "https://0s5qqr11v3.execute-api.us-east-1.amazonaws.com/Prod/s3/buckets"
headers = {"API-Key": "test-api-key-123"}

response = requests.get(url, headers=headers)
buckets = response.json()
print(buckets)
```

### Crear Bucket

Crea un nuevo bucket S3.

**Método:** POST  
**Ruta:** `/s3/buckets`  
**Body:**
```json
{
  "bucket_name": "nombre-del-bucket"
}
```

**Ejemplo de respuesta:**
```json
{
  "name": "nombre-del-bucket"
}
```

**Ejemplo en Python:**
```python
import requests

url = "https://0s5qqr11v3.execute-api.us-east-1.amazonaws.com/Prod/s3/buckets"
headers = {
    "Content-Type": "application/json",
    "API-Key": "test-api-key-123"
}
data = {
    "bucket_name": "mi-nuevo-bucket"
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result)
```

### Listar Objetos en un Bucket

Obtiene la lista de todos los objetos en un bucket específico.

**Método:** GET  
**Ruta:** `/s3/buckets/{bucket_name}/objects`  

**Ejemplo de respuesta:**
```json
[
  {
    "key": "archivo.txt",
    "size": 1024,
    "last_modified": "2025-06-25 19:16:32+00:00"
  }
]
```

**Ejemplo en Python:**
```python
import requests

bucket_name = "mi-bucket"
url = f"https://0s5qqr11v3.execute-api.us-east-1.amazonaws.com/Prod/s3/buckets/{bucket_name}/objects"
headers = {"API-Key": "test-api-key-123"}

response = requests.get(url, headers=headers)
objects = response.json()
print(objects)
```

### Subir Objeto

Sube un archivo a un bucket específico.

**Método:** POST  
**Ruta:** `/s3/buckets/{bucket_name}/objects`  
**Body:**
```json
{
  "file_content": "base64_encoded_content",
  "file_name": "nombre_archivo.txt"
}
```

**Ejemplo de respuesta:**
```json
{
  "message": "File nombre_archivo.txt uploaded successfully to bucket-name",
  "url": "https://bucket-name.s3.amazonaws.com/nombre_archivo.txt",
  "s3_uri": "s3://bucket-name/nombre_archivo.txt"
}
```

**Ejemplo en Python:**
```python
import requests
import base64

bucket_name = "mi-bucket"
url = f"https://0s5qqr11v3.execute-api.us-east-1.amazonaws.com/Prod/s3/buckets/{bucket_name}/objects"
headers = {
    "Content-Type": "application/json",
    "API-Key": "test-api-key-123"
}

# Leer y codificar el archivo en base64
with open("archivo_local.txt", "rb") as file:
    file_content = base64.b64encode(file.read()).decode('utf-8')

data = {
    "file_content": file_content,
    "file_name": "archivo_subido.txt"
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result)
```

### Descargar Objeto

Descarga un archivo específico de un bucket.

**Método:** GET  
**Ruta:** `/s3/buckets/{bucket_name}/objects/`  
**Query Parameters:** `object_key=nombre_archivo.txt`  

**Respuesta:** El contenido del archivo como stream binario.

**Ejemplo en Python:**
```python
import requests

bucket_name = "mi-bucket"
object_key = "archivo.txt"
url = f"https://0s5qqr11v3.execute-api.us-east-1.amazonaws.com/Prod/s3/buckets/{bucket_name}/objects/"
params = {"object_key": object_key}
headers = {"API-Key": "test-api-key-123"}

response = requests.get(url, headers=headers, params=params)

# Guardar el archivo descargado
with open("archivo_descargado.txt", "wb") as file:
    file.write(response.content)
```

### Eliminar Objeto

Elimina un archivo específico de un bucket.

**Método:** DELETE  
**Ruta:** `/s3/buckets/{bucket_name}/objects/`  
**Query Parameters:** `object_key=nombre_archivo.txt`  

**Ejemplo de respuesta:**
```json
{
  "message": "Object nombre_archivo.txt deleted successfully from bucket-name"
}
```

**Ejemplo en Python:**
```python
import requests

bucket_name = "mi-bucket"
object_key = "archivo.txt"
url = f"https://0s5qqr11v3.execute-api.us-east-1.amazonaws.com/Prod/s3/buckets/{bucket_name}/objects/"
params = {"object_key": object_key}
headers = {"API-Key": "test-api-key-123"}

response = requests.delete(url, headers=headers, params=params)
result = response.json()
print(result)
```

### Generar URL Prefirmada

Genera una URL prefirmada para acceder a un objeto por un tiempo limitado sin necesidad de autenticación.

**Método:** GET  
**Ruta:** `/s3/buckets/{bucket_name}/objects/presigned/`  
**Query Parameters:** 
- `object_key=nombre_archivo.txt`
- `expiration=3600` (opcional, tiempo en segundos, por defecto 3600)

**Ejemplo de respuesta:**
```json
{
  "presigned_url": "https://bucket-name.s3.amazonaws.com/archivo.txt?AWSAccessKeyId=..."
}
```

**Ejemplo en Python:**
```python
import requests

bucket_name = "mi-bucket"
object_key = "archivo.txt"
url = f"https://0s5qqr11v3.execute-api.us-east-1.amazonaws.com/Prod/s3/buckets/{bucket_name}/objects/presigned/"
params = {
    "object_key": object_key,
    "expiration": 7200  # 2 horas
}
headers = {"API-Key": "test-api-key-123"}

response = requests.get(url, headers=headers, params=params)
result = response.json()
presigned_url = result["presigned_url"]
print(f"URL prefirmada: {presigned_url}")
```

### Descargar Múltiples Objetos como ZIP

Descarga múltiples archivos de un bucket comprimidos en formato ZIP.

**Método:** GET  
**Ruta:** `/s3/buckets/{bucket_name}/objects/download-zip/`  
**Query Parameters:** `object_keys=archivo1.txt&object_keys=archivo2.txt`  

**Respuesta:** Archivo ZIP como stream binario.

**Ejemplo en Python:**
```python
import requests

bucket_name = "mi-bucket"
object_keys = ["archivo1.txt", "archivo2.txt", "carpeta/archivo3.txt"]
url = f"https://0s5qqr11v3.execute-api.us-east-1.amazonaws.com/Prod/s3/buckets/{bucket_name}/objects/download-zip/"

params = {"object_keys": object_keys}
headers = {"API-Key": "test-api-key-123"}

response = requests.get(url, headers=headers, params=params)

# Guardar el archivo ZIP descargado
with open("archivos.zip", "wb") as file:
    file.write(response.content)
```

## Códigos de Estado HTTP

- **200 OK**: La solicitud se completó correctamente.
- **400 Bad Request**: Error en la solicitud (formato incorrecto, parámetros faltantes).
- **401 Unauthorized**: API Key inválida o faltante.
- **404 Not Found**: Recurso no encontrado.
- **500 Internal Server Error**: Error en el servidor.

## Ejemplo de Cliente Python Completo

```python
import requests
import base64
import json

class S3ApiClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {"API-Key": api_key}
        self.json_headers = {**self.headers, "Content-Type": "application/json"}
    
    def list_buckets(self):
        url = f"{self.base_url}/s3/buckets"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def create_bucket(self, bucket_name):
        url = f"{self.base_url}/s3/buckets"
        data = {"bucket_name": bucket_name}
        response = requests.post(url, headers=self.json_headers, json=data)
        return response.json()
    
    def list_objects(self, bucket_name):
        url = f"{self.base_url}/s3/buckets/{bucket_name}/objects"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def upload_file(self, bucket_name, file_path, file_name=None):
        if file_name is None:
            import os
            file_name = os.path.basename(file_path)
        
        url = f"{self.base_url}/s3/buckets/{bucket_name}/objects"
        
        with open(file_path, "rb") as file:
            file_content = base64.b64encode(file.read()).decode('utf-8')
        
        data = {
            "file_content": file_content,
            "file_name": file_name
        }
        
        response = requests.post(url, headers=self.json_headers, json=data)
        return response.json()
    
    def download_file(self, bucket_name, object_key, save_path):
        url = f"{self.base_url}/s3/buckets/{bucket_name}/objects/"
        params = {"object_key": object_key}
        
        response = requests.get(url, headers=self.headers, params=params)
        
        with open(save_path, "wb") as file:
            file.write(response.content)
        
        return {"status": "success", "path": save_path}
    
    def delete_file(self, bucket_name, object_key):
        url = f"{self.base_url}/s3/buckets/{bucket_name}/objects/"
        params = {"object_key": object_key}
        
        response = requests.delete(url, headers=self.headers, params=params)
        return response.json()
    
    def get_presigned_url(self, bucket_name, object_key, expiration=3600):
        url = f"{self.base_url}/s3/buckets/{bucket_name}/objects/presigned/"
        params = {"object_key": object_key, "expiration": expiration}
        
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
    
    def download_zip(self, bucket_name, object_keys, save_path):
        url = f"{self.base_url}/s3/buckets/{bucket_name}/objects/download-zip/"
        params = {"object_keys": object_keys}
        
        response = requests.get(url, headers=self.headers, params=params)
        
        with open(save_path, "wb") as file:
            file.write(response.content)
        
        return {"status": "success", "path": save_path}

# Ejemplo de uso
if __name__ == "__main__":
    client = S3ApiClient(
        base_url="https://0s5qqr11v3.execute-api.us-east-1.amazonaws.com/Prod",
        api_key="test-api-key-123"
    )
    
    # Listar buckets
    buckets = client.list_buckets()
    print(f"Buckets disponibles: {json.dumps(buckets, indent=2)}")
    
    # Crear un bucket
    new_bucket = client.create_bucket("mi-bucket-de-prueba")
    print(f"Bucket creado: {new_bucket}")
    
    # Subir un archivo
    upload_result = client.upload_file(
        bucket_name="mi-bucket-de-prueba",
        file_path="archivo_local.txt"
    )
    print(f"Archivo subido: {upload_result}")
    
    # Obtener URL prefirmada
    presigned = client.get_presigned_url(
        bucket_name="mi-bucket-de-prueba",
        object_key="archivo_local.txt",
        expiration=7200
    )
    print(f"URL prefirmada: {presigned['presigned_url']}")
```