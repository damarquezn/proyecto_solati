import logging
import os
from datetime import datetime
from .config import LOGS_DIR

def setup_logger():
    """
    Configura el sistema de logging para la aplicación
    
    Returns:
        logging.Logger: Logger configurado
    """
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    log_file = os.path.join(LOGS_DIR, f'app_{datetime.now().strftime("%Y%m%d")}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ],
        force=True
    )
    
    return logging.getLogger(__name__)