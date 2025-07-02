def validar_nomenclatura(archivo):
    if '-' not in archivo or '.' not in archivo:
        return False
    
    nombre_sin_ext = archivo.rsplit('.', 1)[0]
    partes = nombre_sin_ext.split('-')
    
    # Debe tener exactamente 4 partes: id_casa-identificacion-telefono-timestamp
    if len(partes) != 4:
        return False
    
    id_casa, identificacion_deudor, telefono, timestamp = partes
    
    # Validar que timestamp sea numérico y tenga al menos 8 dígitos
    if not timestamp.isdigit() or len(timestamp) < 8:
        return False
    
    # Validar que identificación y teléfono sean numéricos
    if not identificacion_deudor.isdigit() or not telefono.isdigit():
        return False
    
    return True