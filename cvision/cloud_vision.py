from cvision.conectar_s3 import conectar_bucket_s3
from google.cloud import vision
import io

# Conecta com o Cloud Vision e detecta o texto na imagem. Retorna um objeto que contém o texto completo e outras infos,
# como a coordenada de cada texto.
# Adaptada de: https://cloud.google.com/vision/docs/ocr?authuser=1#vision_text_detection-python
def conectar_cloud_vision_e_detectar_texto(path, origem='s3',bucket_name='beep-production'):
    """Conecta com o Cloud Vision e detecta o texto na imagem, com suas coordenadas."""

    client = vision.ImageAnnotatorClient()
    # Caso origem = 's3', conecta com o s3
    if origem == 's3':
        bucket = conectar_bucket_s3(bucket_name)
        obj = bucket.Object(path)
        file_obj = obj.get()
        content = file_obj["Body"].read()
        
    elif origem == 'local':
        with io.open(path, 'rb') as image_file:
            content = image_file.read()
    else:
        raise Exception('Origem deve ser "s3" ou "local".')
    
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
        
    return texts


def extrair_texto_cloud_vision(response):
    """Recebe o texto detectado (que inclui coordenadas e outros parametros) e extrai apenas o texto."""
    try:
        texto_extraido = response[0].description
    except:
        texto_extraido = 'N/A'
    return texto_extraido