import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        
        # Asumo que enviarás 'bucket_name' y 'directorio_name'
        bucket_name = body['bucket_name']
        directorio_name = body['directorio_name']
        
        # Asegurar que el nombre del directorio termine con /
        if not directorio_name.endswith('/'):
            directorio_name += '/'
            
        logger.info(f"Creando directorio '{directorio_name}' en bucket '{bucket_name}'")

        # Crear un objeto vacío con el nombre del directorio
        s3.put_object(
            Bucket=bucket_name,
            Key=directorio_name,
            Body=''
        )
        
        message = f"Directorio '{directorio_name}' creado exitosamente en '{bucket_name}'."
        logger.info(message)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': message})
        }

    except KeyError as e:
        logger.error(f"Falta el parámetro: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f"Falta el parámetro requerido: {str(e)}"})
        }
    except Exception as e:
        logger.error(f"Error al crear el directorio: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }