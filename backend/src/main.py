from core.imprimir import imprimir_resumen_audios
from core.recorrer import recorrer_archivos
from core.subir_s3 import subir_archivo_individual, subir_carpeta_especifica, subir_todas_las_carpetas
from core.listar_s3 import listar_buckets, listar_objetos_bucket
from core.borrar_s3 import borrar_archivo_s3, borrar_multiples_archivos_s3
from core.config import RUTA_SFTP, DEFAULT_BUCKET
import argparse

def main():
    parser = argparse.ArgumentParser(description='Gestión de archivos de audio')
    parser.add_argument('--subir-todo', action='store_true', help='Subir todas las carpetas a S3')
    parser.add_argument('--subir-carpeta', type=str, help='Subir una carpeta específica a S3')
    parser.add_argument('--subir-archivo', type=str, help='Subir un archivo individual a S3 (carpeta/archivo.ext)')
    parser.add_argument('--listar-buckets', action='store_true', help='Listar buckets disponibles')
    parser.add_argument('--listar-objetos', action='store_true', help='Listar objetos en el bucket')
    parser.add_argument('--borrar', type=str, help='Borrar un archivo específico de S3 (especifica la clave del objeto)')
    parser.add_argument('--bucket', type=str, default=DEFAULT_BUCKET, help='Nombre del bucket S3')
    args = parser.parse_args()
    
    # Si no se especifica ninguna acción, mostrar mensaje de ayuda
    if not (args.subir_todo or args.subir_carpeta or args.subir_archivo or args.listar_buckets or args.listar_objetos or args.borrar):
        print("\nNinguna acción especificada. Opciones disponibles:")
        print(f"Bucket por defecto: {DEFAULT_BUCKET}")
        print("Ejemplos:")
        print("  python src/main.py --subir-todo")
        print("  python src/main.py --subir-carpeta mi_carpeta")
        print("  python src/main.py --subir-archivo carpeta/archivo.mp3")
        print("  python src/main.py --listar-objetos")
        print("  python src/main.py --borrar carpeta/archivo.mp3\n")
        parser.print_help()
    
    if args.listar_buckets:
        print("\nBuckets disponibles:")
        buckets = listar_buckets()
        for bucket in buckets:
            print(f"  - {bucket['name']}")
        return
    
    if args.listar_objetos:
        print(f"\nObjetos en el bucket '{args.bucket}':")
        try:
            objetos = listar_objetos_bucket(args.bucket)
            for obj in objetos:
                print(f"  - {obj['key']} ({obj['size']} bytes, modificado: {obj['last_modified']})")
        except Exception as e:
            print(f"Error al listar objetos: {str(e)}")
        return
    
    if args.borrar:
        print(f"\nEliminando archivo '{args.borrar}' del bucket '{args.bucket}'...")
        resultado = borrar_archivo_s3(args.bucket, args.borrar)
        if resultado['estado'] == 'eliminado':
            print(f"\n✓ Archivo eliminado exitosamente: {args.borrar}")
        else:
            print(f"\n✗ Error al eliminar archivo: {resultado['mensaje']}")
        return
    
    if args.subir_archivo:
        import os
        ruta_archivo = os.path.join(RUTA_SFTP, args.subir_archivo)
        print(f"\nSubiendo archivo individual: {args.subir_archivo}")
        resultado = subir_archivo_individual(ruta_archivo, args.bucket)
        if resultado['estado'] == 'subido':
            print(f"✓ {resultado['archivo']} - {resultado['s3_uri']}")
        else:
            print(f"✗ Error: {resultado['mensaje']}")
        return
    
    if args.subir_carpeta:
        print(f"\nSubiendo carpeta: {args.subir_carpeta}")
        resultado = subir_carpeta_especifica(args.subir_carpeta, args.bucket)
        if 'archivos' in resultado:
            print(f"\nCarpeta: {resultado['carpeta']}")
            for archivo in resultado['archivos']:
                if archivo['estado'] == 'subido':
                    print(f"  ✓ {archivo['archivo']} - {archivo['s3_uri']}")
                else:
                    print(f"  ✗ {archivo['archivo']} - Error: {archivo['mensaje']}")
        else:
            print(f"✗ Error: {resultado['mensaje']}")
        return
    
    if args.subir_todo:
        audios_por_carpeta = recorrer_archivos(RUTA_SFTP)
        imprimir_resumen_audios(audios_por_carpeta)
        
        print(f"\nSubiendo todas las carpetas a S3 (bucket: {args.bucket})...")
        print("Este proceso puede tardar dependiendo del tamaño y cantidad de archivos.")
        resultados = subir_todas_las_carpetas(args.bucket)
        
        print("\nResultados de la subida a S3:")
        for carpeta, resultado in resultados.items():
            print(f"\nCarpeta: {carpeta}")
            if 'archivos' in resultado:
                for archivo in resultado['archivos']:
                    if archivo['estado'] == 'subido':
                        print(f"  ✓ {archivo['archivo']} - {archivo['s3_uri']}")
                    else:
                        print(f"  ✗ {archivo['archivo']} - Error: {archivo['mensaje']}")
            else:
                print(f"  ✗ Error: {resultado['mensaje']}")
        return
    
    # Si no hay acción de subida, solo mostrar resumen
    audios_por_carpeta = recorrer_archivos(RUTA_SFTP)
    imprimir_resumen_audios(audios_por_carpeta)

if __name__ == "__main__":
    main()

