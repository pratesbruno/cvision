from cvision.carteirinha import CarteirinhaSaude
import os
import pandas as pd
import json
import requests

<<<<<<< HEAD
def extrair_infos_carteirinha(event={}, context={}):
    # Definir credenciais GCP
=======
def extrair_infos_carteirinha(event=None):
    """Função lambda que extrai as informações das carteirinhas de plano de saúde.
       Para funcionar, deve receber um evento que contém o path da carteirinha no S3."""

    # Definir credenciais GCP a partir do arquivo .json
>>>>>>> master
    path_atual = os.getcwd()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_atual + '/credenciais-gcp-datateam.json'
    
    # Criar df_operadoras_planos a partir do arquivo csv
    df_operadoras_planos = pd.read_csv(path_atual + '/base-operadoras-planos.csv',delimiter=';')

    # Bucket name - passar como argumento?
    bucket_name = 'beep-production'

    event_data = event
    
    if 'body' in event_data:
        event_data = json.loads(event_data['body'])
        
    path_s3 = event_data['path']

    carteirinha_s3 = CarteirinhaSaude(path_s3,df_operadoras_planos,'s3',bucket_name)
    carteirinha_s3.extrair_operadora_plano_num_carteirinha()

    response = {
<<<<<<< HEAD
        'operadora' : carteirinha_s3.operadora,
        'score_operadora' : float(carteirinha_s3.score_operadora),
        'plano' : carteirinha_s3.plano,
        'id_plano' : int(carteirinha_s3.id_plano),
        'score_plano' : float(carteirinha_s3.score_plano),
        'num_carteirinha' : carteirinha_s3.num_carteirinha
=======
        "operadora" : carteirinha_s3.operadora,
        "score_operadora" : carteirinha_s3.score_operadora,
        "plano" : carteirinha_s3.plano,
        "id_plano" : carteirinha_s3.id_plano,
        "score_plano" : carteirinha_s3.score_plano,
        "num_carteirinha" : carteirinha_s3.num_carteirinha
>>>>>>> master
    }

    return {
        'statusCode': 200,
        'body': response
    }
