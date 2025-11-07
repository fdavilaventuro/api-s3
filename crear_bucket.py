import json
import boto3
import logging

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicializar cliente de S3
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # 1. Parsear el body de la solicitud
        body = json.loads(event['body'])
        
        # 2. Obtener el nombre del bucket (coincide con tu curl)
        bucket_name = body['bucket_name']
        
        logger.info(f"Intentando crear el bucket: {bucket_name}")

        # 3. Crear el bucket
        # Nota: El rol IAM (LabRole) debe tener el permiso s3:CreateBucket
        # Para us-east-1, no se necesita LocationConstraint
        s3.create_bucket(Bucket=bucket_name)
        
        message = f"Bucket '{bucket_name}' creado exitosamente."
        logger.info(message)
        
        # 4. Enviar respuesta exitosa
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' # Habilitar CORS
            },
            'body': json.dumps({'message': message})
        }
        
    except json.JSONDecodeError:
        logger.error("Error: El cuerpo de la solicitud no es un JSON válido.")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Cuerpo de la solicitud mal formado (JSON inválido).'})
        }
    except KeyError:
        logger.error("Error: 'bucket_name' no se encontró en el cuerpo de la solicitud.")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': "Falta el parámetro 'bucket_name' en el cuerpo."})
        }
    except Exception as e:
        logger.error(f"Error al crear el bucket: {str(e)}")
        # Manejar errores comunes de S3
        if 'BucketAlreadyOwnedByYou' in str(e):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f"El bucket '{bucket_name}' ya existe y te pertenece."})
            }
        if 'BucketAlreadyExists' in str(e):
             return {
                'statusCode': 409, # Conflict
                'body': json.dumps({'error': f"El nombre del bucket '{bucket_name}' ya está en uso."})
            }
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }