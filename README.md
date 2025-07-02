# Proyecto Solati - Gestión de Grabaciones

Este proyecto permite gestionar archivos de grabación de audio, incluyendo:
- Listar archivos de grabación locales
- Mostrar información detallada de cada archivo
- Subir archivos a Amazon S3
- Listar buckets y objetos en S3

## Requisitos

- Python 3.6+
- Bibliotecas: pandas, requests
mutagen

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd proyecto_solati

# Instalar dependencias
pip install -r requerimientos.txt
```

## Uso

### Listar archivos locales

```bash
python src/main.py
```

### Subir archivos a S3

```bash
python src/main.py --subir --bucket nombre-del-bucket
```

### Listar buckets disponibles

```bash
python src/main.py --listar-buckets
```

### Listar objetos en un bucket

```bash
python src/main.py --listar-objetos --bucket nombre-del-bucket
```

## Estructura del proyecto

```
proyecto_solati/
├── data/                # Datos adicionales
├── docs/                # Documentación
├── logs/                # Archivos de registro
├── simulador-SFTP/      # Archivos de audio simulados
├── src/                 # Código fuente
│   ├── core/            # Módulos principales
│   │   ├── config.py    # Configuración
│   │   ├── duracion.py  # Extracción de duración
│   │   ├── fecha.py     # Manejo de fechas
│   │   ├── formato.py   # Detección de formato
│   │   ├── imprimir.py  # Visualización de datos
│   │   ├── listar_s3.py # Operaciones de listado en S3
│   │   ├── recorrer.py  # Recorrido de archivos
│   │   ├── s3_client.py # Cliente API de S3
│   │   ├── subir_s3.py  # Subida de archivos a S3
│   │   └── validar.py   # Validación de archivos
│   └── main.py          # Punto de entrada
└── requerimientos.txt   # Dependencias
```