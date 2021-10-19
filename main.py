from cvision.carteirinha import CarteirinhaSaude
import os
import pandas as pd
import json
import requests

def extrair_infos_carteirinha(event=None):
    
    # Definir credenciais GCP
    path_atual = os.getcwd()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_atual + '/credenciais-gcp.json'
    
    # Criar df_op_planos de arquivo csv
    df_operadoras_planos = pd.read_csv(path_atual + '/base-operadoras-planos.csv',delimiter=';')
    
    #path_s3 = 'uploads/attachment/file/606217/image_picker8860528620762238448_compressed9143976869443367171.jpg'
    bucket_name = 'beep-production'

    # json.loads funciona para testes locais. event.get_json() para cloud.
    try:
        event_json = json.loads(event)
    except:
        event_json = event.get_json()

    path_s3 = event_json['path']

    carteirinha_s3 = CarteirinhaSaude(path_s3,df_operadoras_planos,'s3',bucket_name)
    carteirinha_s3.extrair_operadora_plano_num_carteirinha()

    response = {
        'operadora' : carteirinha_s3.operadora,
        'score_operadora' : carteirinha_s3.score_operadora,
        'plano' : carteirinha_s3.plano,
        'id_plano' : carteirinha_s3.id_plano,
        'score_plano' : carteirinha_s3.score_plano,
        'num_carteirinha' : carteirinha_s3.num_carteirinha
    }

    print(response)
    return str(response)
