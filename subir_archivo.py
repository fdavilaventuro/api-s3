import json
import boto3
import base64 # Importante para decodificar
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        
        # Claves basadas en la sugerencia de curl anterior
        bucket_name = body['bucket_name']
        file_name = body['file_name'] # ej: 'mi/ruta/archivo.txt'
        file_content_base64 = body['file_content_base64']

        # 1. Decodificar el contenido del archivo de Base64
        try:
            file_content = base64.b64decode(file_content_base64)
        except Exception as e:
            logger.error(f"Error al decodificar Base64: {str(e)}")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'El contenido del archivo (file_content_base64) no es un Base64 válido.'})
            }

        logger.info(f"Subiendo archivo '{file_name}' al bucket '{bucket_name}'")

        # 2. Subir el objeto (binario) a S3
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_content
        )
        
        message = f"Archivo '{file_name}' subido exitosamente a '{bucket_name}'."
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
        logger.error(f"Error al subir el archivo: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }