from unicodedata import normalize

def remover_espacos(string):
    return ''.join(string.split())

def remover_pontos_e_hifens(string):
    string = string.replace('-','')
    return string.replace('.','')

def remover_acentos(string):
    string_sem_acentos = normalize('NFKD', string).encode('ASCII','ignore').decode('ASCII')
    return(string_sem_acentos)

def tratar_string(string):
    string = remover_espacos(string)
    string = remover_pontos_e_hifens(string)
    string = remover_acentos(string)
    string = string.replace('|','I') # O OCR as vezes identifica "I" como "|"
    return string.lower()

def listar_todas_operadoras(df_operadoras_planos):
    """Lista as operadoras distintas do df de operadoras e planos."""
    return list(df_operadoras_planos['operadora'].unique())

def listar_planos_de_operadora(operadora, df_operadoras_planos):
    """Lista os planos distintos de determinada operadora."""
    return df_operadoras_planos['string_alvo'][df_operadoras_planos['operadora']==operadora]
