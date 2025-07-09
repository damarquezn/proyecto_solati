import logging
import os
from datetime import datetime
from .config import LOGS_DIR

def setup_logger(cliente_name=None):
    """
    Configura el sistema de logging para la aplicación
    
    Args:
        cliente_name (str, optional): Nombre del cliente para logs separados
    
    Returns:
        logging.Logger: Logger configurado
    """
    # Determinar carpeta de logs según cliente
    if cliente_name:
        client_logs_dir = os.path.join(LOGS_DIR, cliente_name)
    else:
        client_logs_dir = os.path.join(LOGS_DIR, 'general')
    
    # Crear directorio del cliente si no existe
    os.makedirs(client_logs_dir, exist_ok=True)
    
    # Ruta completa del archivo de log
    log_file = os.path.join(client_logs_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
    
    # Configurar formato y archivo
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ],
        force=True
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logger configurado para cliente: {cliente_name or 'general'}")
    logger.info(f"Archivo de log: {log_file}")
    
    return logger