DOCUMENTO DE ALCANCE Y 
REQUERIMIENTOS 
Sistema de Almacenamiento y Consulta de Grabaciones 
de Llamadas 
Versión: 1.0 
Fecha: 11 de junio de 2025 
Proyecto: Sistema SaaS de Grabaciones Telefónicas 
1. DESCRIPCIÓN GENERAL DEL PROYECTO 
Este documento define los requerimientos para desarrollar un sistema que permita recibir, 
almacenar y consultar grabaciones de llamadas telefónicas de múltiples casas de cobranza 
contratadas por una empresa matriz. El sistema operará bajo el modelo SaaS y utilizará AWS 
S3 como repositorio principal de archivos, sin implementar persistencia de datos 
estructurados. 
El flujo principal consiste en que las casas de cobranza (proveedores externos) transmitan sus 
grabaciones mediante SFTP, un proceso automatizado las procese y almacene en AWS S3, y 
finalmente una interfaz web permita a la empresa matriz buscar, reproducir y descargar estas 
grabaciones con identificación clara del origen (casa de cobranza). 
2. ARQUITECTURA TÉCNICA PROPUESTA 
Basándose en el diagrama conceptual proporcionado, el sistema se compone de cuatro 
componentes principales: 
Componente 1: Servidor SFTP de Recepción 
Punto de entrada donde las casas de cobranza (Emp1, Emp2, Emp3, etc.) depositan sus 
archivos de grabaciones mediante protocolo SFTP seguro. 
Componente 2: Proceso de Clasificación (Python/Botocore) 
Servicio automatizado que monitorea el servidor SFTP, procesa los archivos recibidos de 
cada casa de cobranza y los organiza según criterios específicos antes de su 
almacenamiento. 
Componente 3: Almacenamiento AWS S3 
Repositorio en la nube donde se almacenan definitivamente las grabaciones organizadas por 
casa de cobranza en buckets y carpetas estructuradas. 
Componente 4: Interfaz Web de Consulta 
Aplicación web que permite a los usuarios de la empresa matriz buscar, reproducir y 
descargar las grabaciones de todas las casas de cobranza contratadas, con clara 
identificación del origen de cada grabación. 
3. REQUERIMIENTOS FUNCIONALES 
3.1 Recepción de Archivos por SFTP 
RF-001: Configuración de Accesos SFTP por Casa de Cobranza 
El sistema debe permitir configurar credenciales SFTP únicas para cada casa de cobranza 
contratada, garantizando que cada casa de cobranza solo pueda acceder a su directorio 
asignado dentro del servidor SFTP. Cada directorio debe estar claramente identificado con el 
código único de la casa de cobranza. 
RF-002: Monitoreo Automático de Directorios por Casa de Cobranza 
El sistema debe implementar un mecanismo de monitoreo continuo que detecte 
automáticamente cuando se depositan nuevos archivos en los directorios SFTP de cada casa 
de cobranza contratada, manteniendo un registro claro del origen de cada archivo. 
RF-003: Validación de Formato de Archivos 
El sistema debe validar que los archivos recibidos correspondan a formatos de audio 
soportados (WAV, MP3, AAC, OGG) y rechazar archivos con formatos no válidos, generando 
logs de error correspondientes. 
RF-004: Control de Convenciones de Nomenclatura por Casa de Cobranza 
El sistema debe verificar que los nombres de archivo sigan la convención establecida: 
id_casa_cobranza-identificaciondeudor-telefono-timestamp_epoch.extension (ejemplo: 
casa_001-123456789-300000000-1717200000.wav), donde timestamp_epoch representa la fecha y hora de la 
grabación en formato Unix timestamp, y el identificador de casa de cobranza permita rastrear 
inequívocamente el origen de cada grabación, identificación representa el número de identificaón del deudor al que se le hizo la llamada, y el número de telefono del deudor al que se le realizó la llamada.  
3.2 Procesamiento y Clasificación 
RF-005: Extracción de Metadatos con Identificación de Origen 
El proceso de clasificación debe extraer metadatos relevantes de cada archivo, incluyendo 
duración de la grabación, formato de audio, tamaño del archivo, casa de cobranza de origen y 
timestamp de creación. Esta información debe ser accesible para la empresa matriz en las 
consultas posteriores. 
RF-006: Organización Jerárquica en S3 por Casa de Cobranza 
El sistema debe organizar los archivos en AWS S3 siguiendo una estructura jerárquica: 
/casa_cobranza/{id_casa}/año/{YYYY}/mes/{MM}/dia/{DD}/archivo.extensio
 n para facilitar las búsquedas y permitir que la empresa matriz identifique rápidamente el 
origen de cada grabación. 
RF-007: Generación de Identificadores Únicos 
Cada grabación debe recibir un identificador único (UUID) que permita su localización 
inequívoca, independientemente de cambios en la estructura de carpetas. 
RF-008: Conversión de Formatos (Opcional) 
El sistema debe tener la capacidad de convertir grabaciones a un formato estándar (por 
ejemplo, MP3 320kbps) para optimizar el almacenamiento y la reproducción web, 
manteniendo también el archivo original si es requerido. 
3.3 Interfaz Web de Consulta 
RF-009: Sistema de Búsqueda Avanzada con Filtros por Casa de Cobranza 
La interfaz web debe permitir a los usuarios de la empresa matriz realizar búsquedas por 
múltiples criterios: casa de cobranza específica, rango de fechas, duración de llamada, y 
combinaciones de estos filtros. La búsqueda debe ejecutarse directamente sobre la 
estructura de carpetas de S3 y mostrar claramente el origen de cada resultado. 
RF-010: Visualización de Resultados con Identificación de Origen 
Los resultados de búsqueda deben presentarse en una tabla paginada que muestre: nombre 
del archivo, casa de cobranza origen, fecha/hora de grabación, duración, tamaño del archivo 
y acciones disponibles (reproducir, descargar). La identificación de la casa de cobranza debe 
ser prominente y clara. 
RF-011: Reproductor de Audio Integrado 
La interfaz debe incluir un reproductor de audio HTML5 que permita escuchar las 
grabaciones directamente en el navegador, con controles de reproducción, pausa, adelanto y 
retroceso. El reproductor debe mostrar claramente qué casa de cobranza generó la 
grabación que se está reproduciendo. 
RF-012: Descarga de Archivos con Identificación de Origen 
Los usuarios de la empresa matriz deben poder descargar grabaciones individuales o 
múltiples grabaciones en un archivo comprimido ZIP. Los archivos descargados deben 
mantener información clara sobre su casa de cobranza de origen, ya sea en el nombre del 
archivo o en la estructura de carpetas del ZIP. 
RF-013: Control de Acceso para Empresa Matriz 
La interfaz web debe implementar un sistema de autenticación que permita a los usuarios 
autorizados de la empresa matriz acceder a todas las grabaciones de todas las casas de 
cobranza contratadas, con capacidad de filtrar y organizar por proveedor específico. 
4. REQUERIMIENTOS NO FUNCIONALES 
4.1 Rendimiento 
RNF-001: Capacidad de Procesamiento 
El sistema debe ser capaz de procesar al menos 1000 archivos de grabaciones por hora sin 
degradación significativa del rendimiento. 
RNF-002: Tiempo de Respuesta Web 
La interfaz web debe cargar los resultados de búsqueda en menos de 5 segundos para 
consultas que retornen hasta 100 registros. 
RNF-003: Streaming de Audio 
La reproducción de audio debe iniciarse en menos de 3 segundos desde que el usuario hace 
clic en reproducir, utilizando técnicas de streaming cuando sea posible. 
4.2 Seguridad 
RNF-004: Cifrado de Transmisión 
Todas las comunicaciones SFTP deben utilizar cifrado SSH/TLS para proteger los archivos 
durante la transmisión. 
RNF-005: Seguridad en AWS S3 
Los buckets de S3 deben configurarse con acceso restringido, utilizando roles IAM 
específicos y cifrado del lado del servidor (SSE-S3). 
RNF-006: Autenticación Web 
La interfaz web debe implementar autenticación robusta (OAuth 2.0 o similar) con sesiones 
seguras y tokens de acceso con tiempo de vida limitado. 
4.3 Disponibilidad 
RNF-007: Disponibilidad del Servicio 
El sistema debe mantener una disponibilidad del 99.5% mensual, excluyendo ventanas de 
mantenimiento programado. 
RNF-008: Recuperación ante Fallos 
El proceso de clasificación debe implementar mecanismos de reintento automático y 
recuperación ante fallos, asegurando que no se pierdan archivos durante el procesamiento. 
5. CONSIDERACIONES TÉCNICAS ESPECÍFICAS 
5.1 Ausencia de Persistencia de Datos 
Dado que el sistema no manejará persistencia tradicional de datos, toda la información sobre 
las grabaciones se derivará dinámicamente de la estructura de carpetas y metadatos de 
archivos en S3. Esto implica que: 
 - Las búsquedas se realizarán mediante consultas directas a la API de S3 
 - Los metadatos se extraerán en tiempo real de los nombres de archivos y propiedades 
de S3 
 - No existirá una base de datos relacional que mantenga índices o referencias 
Esta aproximación simplifica la arquitectura pero requiere una estructura de carpetas muy 
bien definida y convenciones de nomenclatura estrictas. 
5.2 Optimización para Búsquedas sin Base de Datos 
Para compensar la ausencia de índices de base de datos, el sistema debe implementar: 
- Cache en memoria de las consultas más frecuentes 
- Algoritmos de búsqueda optimizados que aprovechen la estructura jerárquica de S3 
- Paginación eficiente para evitar cargar grandes cantidades de datos innecesariamente 
6. FLUJO DE DATOS DETALLADO 
Paso 1: Recepción 
La empresa cliente deposita archivos en su directorio SFTP específico siguiendo la 
convención de nomenclatura establecida. 
Paso 2: Detección 
El proceso de monitoreo detecta nuevos archivos y los coloca en una cola de procesamiento 
para evitar conflictos de acceso concurrente. 
Paso 3: Validación 
Se valida el formato, nomenclatura y integridad de cada archivo. Los archivos que no 
cumplan las validaciones se mueven a una carpeta de errores. 
Paso 4: Procesamiento 
Se extraen metadatos, se genera el UUID único y se determina la ubicación final en S3 
basada en la fecha y empresa. 
Paso 5: Almacenamiento 
El archivo se carga a S3 en la ubicación determinada, con metadatos adicionales como tags 
de S3. 
Paso 6: Limpieza 
Una vez confirmado el almacenamiento exitoso en S3, el archivo se elimina del servidor SFTP 
para liberar espacio. 
7. CRITERIOS DE ACEPTACIÓN 
Para considerar el sistema completamente funcional, debe cumplir con los siguientes 
criterios: 
Criterio 1: Ingesta Automatizada desde Casas de Cobranza 
El sistema debe procesar exitosamente archivos de prueba depositados por SFTP de al 
menos 3 casas de cobranza diferentes, organizándolos correctamente en S3 con 
identificación clara del origen. 
Criterio 2: Búsqueda Funcional con Visibilidad Total 
La interfaz web debe permitir a la empresa matriz encontrar grabaciones específicas usando 
filtros de casa de cobranza, fecha y duración, retornando resultados precisos de todas las 
casas contratadas en menos de 5 segundos. 
Criterio 3: Reproducción y Descarga con Trazabilidad 
Los usuarios de la empresa matriz deben poder reproducir grabaciones directamente en el 
navegador y descargar archivos individuales o múltiples, manteniendo siempre la 
identificación clara de qué casa de cobranza generó cada grabación. 
Criterio 4: Visibilidad Completa para Empresa Matriz 
La empresa matriz debe poder acceder a todas las grabaciones de todas las casas de 
cobranza contratadas, con capacidad de filtrar, organizar y administrar el contenido de forma 
centralizada. 
8. ENTREGABLES ESPERADOS 
Entregable 1: Servidor SFTP Configurado 
Servidor SFTP operativo con directorios segregados por empresa y credenciales de acceso 
configuradas. 
Entregable 2: Servicio de Procesamiento 
Aplicación Python/Botocore que monitoree, valide y transfiera archivos a S3 de forma 
automatizada. 
Entregable 3: Interfaz Web Completa 
Aplicación web responsiva con funcionalidades de búsqueda, reproducción y descarga 
implementadas. 
Entregable 4: Documentación Técnica 
Manual de instalación, configuración y operación del sistema, incluyendo procedimientos de 
mantenimiento y resolución de problemas. 
Entregable 5: Scripts de Despliegue 
Scripts automatizados para el despliegue en ambiente de producción, incluyendo 
configuración de infraestructura AWS necesaria. 
9. SUPUESTOS Y RESTRICCIONES 
Supuestos: 
- Las empresas cliente tienen capacidad técnica para utilizar SFTP 
- Los archivos de grabaciones no excederán 500 MB por archivo individual 
- El volumen total de grabaciones no superará 10 TB por empresa por año 
- Los formatos de audio serán estándar y compatibles con reproductores web 
Restricciones: 
- No se implementará transcripción automática de las grabaciones 
- El sistema no incluirá funcionalidades de análisis de sentimientos o inteligencia 
artificial 
- La retención de grabaciones será responsabilidad de políticas de S3, no del sistema 
aplicativo 
- No se desarrollarán aplicaciones móviles en esta fase inicial 