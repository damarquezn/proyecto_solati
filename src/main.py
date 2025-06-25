from core.imprimir import imprimir_resumen_audios
from core.recorrer import recorrer_archivos
from core.config import RUTA_SFTP

if __name__ == "__main__":
    audios_por_carpeta = recorrer_archivos(RUTA_SFTP)
    imprimir_resumen_audios(audios_por_carpeta)

