import os
import pandas as pd
from .duracion import extraer_duracion_segundos
from .fecha import convertir_timestamp_a_humano
from .config import RUTA_SFTP

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
                        'Casa de Cobranza': nombre_carpeta,
                        'Archivo': audio,
                        'ID Deudor': partes[1],
                        'Teléfono': partes[2],
                        'Fecha': fecha_humana,
                        'Duración (seg)': duracion
                    })
        else:
            datos.append({
                'Casa de Cobranza': nombre_carpeta,
                'Archivo': '(sin archivos)',
                'ID Deudor': '-',
                'Teléfono': '-',
                'Fecha': '-',
                'Duración (seg)': 0
            })

    df = pd.DataFrame(datos)
    print(df.to_string(index=False))