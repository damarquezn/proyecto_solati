import os
import pandas as pd
from .duracion import extraer_duracion_segundos
from .fecha import convertir_timestamp_a_humano
from .formato import obtener_formato
from .config import RUTA_SFTP
from .tamano import obtener_tamano_archivo as tamano_archivo, formatear_tamano   

def imprimir_resumen_audios(diccionario_audios):
    datos = []
    
    for nombre_carpeta, audios in diccionario_audios.items():
        if audios:
            for audio in audios:
                nombre_sin_ext = audio.rsplit('.', 1)[0]
                partes = nombre_sin_ext.split('-')
                if len(partes) == 4:
                    timestamp = partes[-1]
                    fecha_humana = convertir_timestamp_a_humano(timestamp)
                    ruta_completa = os.path.join(RUTA_SFTP, nombre_carpeta, audio)
                    duracion = extraer_duracion_segundos(ruta_completa)
                    
                    datos.append({
                        'Archivo de grabación': audio,
                        'Casa de Cobranza': nombre_carpeta,
                        'ID Deudor': partes[1],
                        'Teléfono': partes[2],
                        'Fecha': fecha_humana,
                        'Duración (seg)': duracion,
                        'Formato': obtener_formato(audio),
                        'Tamaño del archivo': formatear_tamano(tamano_archivo(ruta_completa))
                    })
        else:
            datos.append({
                'Archivo de grabación': '(sin archivos)',
                'Casa de Cobranza': nombre_carpeta,
                'ID Deudor': '-',
                'Teléfono': '-',
                'Fecha': '-',
                'Duración (seg)': 0,
                'Formato': '-',
                'Tamaño del archivo': '0 B'
            })

    df = pd.DataFrame(datos)
    print(df.to_string(index=False))