import requests
import base64
import os

headers = {
    "API-Key": "test-api-key-123",
    "Content-Type": "application/json"
}

# URL base
base_url = "https://0s5qqr11v3.execute-api.us-east-1.amazonaws.com/Prod"

# 1. Listar buckets
def listar_buckets():
    url = f"{base_url}/s3/buckets"
    try:
        response = requests.get(url, headers=headers)
        print("Status:", response.status_code)
        print("Buckets:", response.text)
        return response.json()
    except Exception as e:
        print("Error:", str(e))
        return None

# 2. Subir archivo
def subir_archivo(bucket_name, ruta_archivo, nombre_destino=None):
    if nombre_destino is None:
        nombre_destino = os.path.basename(ruta_archivo)
    
    url = f"{base_url}/s3/buckets/{bucket_name}/objects"
    
    # Leer archivo y codificar en base64
    with open(ruta_archivo, "rb") as file:
        file_content = base64.b64encode(file.read()).decode('utf-8')
    
    # Preparar datos para la API
    data = {
        "file_content": file_content,
        "file_name": nombre_destino
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print("Status:", response.status_code)
        print("Respuesta:", response.text)
        return response.json()
    except Exception as e:
        print("Error:", str(e))
        return None

# 3. Listar objetos en un bucket
def listar_objetos(bucket_name):
    url = f"{base_url}/s3/buckets/{bucket_name}/objects"
    try:
        response = requests.get(url, headers=headers)
        print("Status:", response.status_code)
        print("Objetos:", response.text)
        return response.json()
    except Exception as e:
        print("Error:", str(e))
        return None

# Ejemplo de uso
if __name__ == "__main__":
    # Listar buckets disponibles
    print("\n=== Listando buckets ===")
    buckets = listar_buckets()
    
    if buckets and len(buckets) > 0:
        bucket_name = buckets[0]["name"]
        print(f"\n=== Usando bucket: {bucket_name} ===")
        
        # Subir un archivo de prueba (reemplaza con una ruta válida)
        ruta_archivo = "simulador-SFTP/konecta/konecta-1007894194-3168976590-1717200000.mp3"
        if os.path.exists(ruta_archivo):
            print(f"\n=== Subiendo archivo: {ruta_archivo} ===")
            resultado = subir_archivo(bucket_name, ruta_archivo)
        
        # Listar objetos en el bucket
        print(f"\n=== Listando objetos en {bucket_name} ===")
        listar_objetos(bucket_name)