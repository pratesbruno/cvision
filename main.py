from cvision.carteirinha import CarteirinhaSaude
import os
import pandas as pd
import json
import requests

def extrair_infos_carteirinha(event={}, context={}):
    # Definir credenciais GCP
    path_atual = os.getcwd()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_atual + '/credenciais-gcp.json'
    
    # Criar df_op_planos de arquivo csv
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
        'operadora' : carteirinha_s3.operadora,
        'score_operadora' : float(carteirinha_s3.score_operadora),
        'plano' : carteirinha_s3.plano,
        'id_plano' : int(carteirinha_s3.id_plano),
        'score_plano' : float(carteirinha_s3.score_plano),
        'num_carteirinha' : carteirinha_s3.num_carteirinha
    }

    return {
        'statusCode': 200,
        'body': response
    }
