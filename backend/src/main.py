from core.imprimir import imprimir_resumen_audios
from core.recorrer import recorrer_archivos
from core.subir_s3 import subir_archivo_individual, subir_carpeta_especifica, subir_todas_las_carpetas
from core.listar_s3 import listar_buckets, listar_objetos_bucket
from core.borrar_s3 import borrar_archivo_s3, borrar_multiples_archivos_s3, borrar_todo_bucket
from core.config import RUTA_SFTP, DEFAULT_BUCKET
from core.logger import setup_logger
import argparse
import os

def main():
    logger = setup_logger()
    logger.info("Iniciando aplicación de gestión de audios")
    
    parser = argparse.ArgumentParser(description='Gestión de archivos de audio')
    parser.add_argument('--subir-todo', action='store_true', help='Subir todas las carpetas a S3')
    parser.add_argument('--subir-carpeta', type=str, help='Subir una carpeta específica a S3')
    parser.add_argument('--subir-archivo', type=str, help='Subir un archivo individual a S3 (carpeta/archivo.ext)')
    parser.add_argument('--listar-buckets', action='store_true', help='Listar buckets disponibles')
    parser.add_argument('--listar-objetos', action='store_true', help='Listar objetos en el bucket')
    parser.add_argument('--borrar', type=str, help='Borrar un archivo específico de S3 (especifica la clave del objeto)')
    parser.add_argument('--borrar-multiples', nargs='+', help='Borrar múltiples archivos de S3 (lista de claves)')
    parser.add_argument('--borrar-todo', action='store_true', help='Borrar todos los objetos del bucket')
    parser.add_argument('--bucket', type=str, default=DEFAULT_BUCKET, help='Nombre del bucket S3')
    parser.add_argument('--ruta', type=str, required=True, help='Ruta local del SFTP (por defecto: %(default)s)')
    args = parser.parse_args()
    args.ruta = os.path.abspath(args.ruta)
    logger.info(f"Ruta de trabajo: {args.ruta}")

    
    if not (args.subir_todo or args.subir_carpeta or args.subir_archivo or args.listar_buckets or args.listar_objetos or args.borrar or args.borrar_multiples or args.borrar_todo):
        print("\nNinguna acción especificada. Opciones disponibles:")
        print(f"Bucket por defecto: {DEFAULT_BUCKET}")
        print("Ejemplos:")
        print("  python src/main.py --subir-todo")
        print("  python src/main.py --subir-carpeta mi_carpeta")
        print("  python src/main.py --subir-archivo carpeta/archivo.mp3")
        print("  python src/main.py --listar-objetos")
        print("  python src/main.py --borrar carpeta/archivo.mp3")
        print("  python src/main.py --borrar-multiples carpeta/archivo1.mp3 carpeta/archivo2.wav")
        print("  python src/main.py --ruta /mi/ruta/audios --borrar-todo\n")
        parser.print_help()
    
    if args.listar_buckets:
        logger.info("Listando buckets disponibles")
        print("\nBuckets disponibles:")
        buckets = listar_buckets()
        for bucket in buckets:
            print(f"  - {bucket['name']}")
        logger.info(f"Se encontraron {len(buckets)} buckets")
        return
    
    if args.listar_objetos:
        logger.info(f"Listando objetos del bucket: {args.bucket}")
        print(f"\nObjetos en el bucket '{args.bucket}':")
        try:
            objetos = listar_objetos_bucket(args.bucket)
            for obj in objetos:
                print(f"  - {obj['key']} ({obj['size']} bytes, modificado: {obj['last_modified']})")
            logger.info(f"Se encontraron {len(objetos)} objetos en el bucket")
        except Exception as e:
            logger.error(f"Error al listar objetos del bucket {args.bucket}: {str(e)}")
            print(f"Error al listar objetos: {str(e)}")
        return
    
    if args.borrar:
        logger.info(f"Iniciando eliminación de archivo: {args.borrar} del bucket: {args.bucket}")
        print(f"\nEliminando archivo '{args.borrar}' del bucket '{args.bucket}'...")
        resultado = borrar_archivo_s3(args.bucket, args.borrar)
        if resultado['estado'] == 'eliminado':
            logger.info(f"Archivo eliminado exitosamente: {args.borrar}")
            print(f"\n✓ Archivo eliminado exitosamente: {args.borrar}")
        else:
            logger.error(f"Error al eliminar archivo {args.borrar}: {resultado['mensaje']}")
            print(f"\n✗ Error al eliminar archivo: {resultado['mensaje']}")
        return
    
    if args.borrar_multiples:
        logger.info(f"Iniciando eliminación múltiple de {len(args.borrar_multiples)} archivos del bucket: {args.bucket}")
        print(f"\nEliminando {len(args.borrar_multiples)} archivos del bucket '{args.bucket}'...")
        resultados = borrar_multiples_archivos_s3(args.bucket, args.borrar_multiples)
        
        exitosos = sum(1 for r in resultados if r['estado'] == 'eliminado')
        errores = len(resultados) - exitosos
        
        logger.info(f"Eliminación múltiple completada: {exitosos} exitosos, {errores} errores")
        print(f"\nResultados:")
        print(f"✓ {exitosos} archivos eliminados exitosamente")
        if errores > 0:
            print(f"✗ {errores} archivos con errores")
            for resultado in resultados:
                if resultado['estado'] == 'error':
                    print(f"  - {resultado['archivo']}: {resultado['mensaje']}")
        return
    
    if args.borrar_todo:
        logger.warning(f"Solicitud de vaciado completo del bucket: {args.bucket}")
        print(f"\nEsto eliminará TODOS los objetos del bucket '{args.bucket}'")
        confirmacion = input("¿Estás seguro? Escribe 'SI' para continuar: ")
        
        if confirmacion != 'SI':
            logger.info("Operación de vaciado cancelada por el usuario")
            print("Operación cancelada.")
            return
        
        logger.info(f"Iniciando vaciado completo del bucket: {args.bucket}")
        print(f"\nVaciando bucket '{args.bucket}'...")
        resultado = borrar_todo_bucket(args.bucket)
        
        if resultado['estado'] == 'vacio':
            logger.info(f"Bucket {args.bucket} ya estaba vacío")
            print(f"✓ {resultado['mensaje']}")
        elif resultado['estado'] == 'completado':
            logger.info(f"Vaciado completado: {resultado['eliminados']} eliminados, {resultado['errores']} errores")
            print(f"\nResultados:")
            print(f"✓ {resultado['eliminados']} archivos eliminados exitosamente")
            if resultado['errores'] > 0:
                print(f"✗ {resultado['errores']} archivos con errores")
        else:
            logger.error(f"Error al vaciar bucket {args.bucket}: {resultado['mensaje']}")
            print(f"✗ Error: {resultado['mensaje']}")
        return
    
    if args.subir_archivo:
        ruta_archivo = os.path.join(args.ruta, args.subir_archivo)
        logger.info(f"Iniciando subida de archivo individual: {args.subir_archivo} al bucket: {args.bucket}")
        print(f"\nSubiendo archivo individual: {args.subir_archivo}")
        resultado = subir_archivo_individual(ruta_archivo, args.bucket)
        if resultado['estado'] == 'subido':
            logger.info(f"Archivo subido exitosamente: {args.subir_archivo}")
            print(f"✓ {resultado['archivo']} - {resultado['s3_uri']}")
        else:
            logger.error(f"Error al subir archivo {args.subir_archivo}: {resultado['mensaje']}")
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
        logger.info(f"Iniciando subida masiva desde ruta: {args.ruta} al bucket: {args.bucket}")
        audios_por_carpeta = recorrer_archivos(args.ruta)
        imprimir_resumen_audios(audios_por_carpeta)
        
        total_archivos = sum(len(archivos) for archivos in audios_por_carpeta.values())
        logger.info(f"Se encontraron {total_archivos} archivos en {len(audios_por_carpeta)} carpetas")
        
        print(f"\nSubiendo todas las carpetas a S3 (bucket: {args.bucket})...")
        print("Este proceso puede tardar dependiendo del tamaño y cantidad de archivos.")
        resultados = subir_todas_las_carpetas(ruta_sftp= args.ruta ,bucket_name=args.bucket)
        
        exitosos_total = 0
        errores_total = 0
        
        print("\nResultados de la subida a S3:")
        for carpeta, resultado in resultados.items():
            print(f"\nCarpeta: {carpeta}")
            if 'archivos' in resultado:
                for archivo in resultado['archivos']:
                    if archivo['estado'] == 'subido':
                        exitosos_total += 1
                        print(f"  ✓ {archivo['archivo']} - {archivo['s3_uri']}")
                    else:
                        errores_total += 1
                        print(f"  ✗ {archivo['archivo']} - Error: {archivo['mensaje']}")
            else:
                print(f"  ✗ Error: {resultado['mensaje']}")
        
        logger.info(f"Subida masiva completada: {exitosos_total} exitosos, {errores_total} errores")
        return
    
    audios_por_carpeta = recorrer_archivos(args.ruta)
    imprimir_resumen_audios(audios_por_carpeta)

if __name__ == "__main__":
    main()

