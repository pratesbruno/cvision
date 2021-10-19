from cvision.utils import tratar_string
import pandas as pd
from difflib import SequenceMatcher

# Dado uma string alvo e um texto, essa função percorre o texto procurando um trecho que corresponda a string alvo.
# A função retorna um valor de 0 a 1. Valores altos significam que foi encontrado um trecho no texto que parece com a string alvo.
# Se a função retornar 1, foi encontrado exatamente a string alvo dentro do texto (desconsidera letras maiusculas e espaços).
def avaliar_ocorrencia_de_string_em_texto(texto, string):
    """Procura uma string em um texto e retorna um score de 0 a 1, onde 1 representa um match perfeito."""
    
    # Remove acentos, espaços, e transforma tudo em letra minuscula.
    string = tratar_string(string)
    texto = tratar_string(texto)
    max_ratio = 0
    
    for i in range(len(texto)-len(string)+1): 
        curr_string = texto[i:i+len(string)] 
        # Computa o "ratio", que corresponde a similariedade entre as strings (usando a biblioteca difflib)
        ratio = SequenceMatcher(None, curr_string, string).ratio()
        max_ratio = ratio if ratio > max_ratio else max_ratio

    return max_ratio

# Dado uma string alvo e um texto, essa função percorre o texto procurando um trecho que corresponda a string alvo.
# A função retorna um valor de 0 a 1. Valores altos significam que foi encontrado um trecho no texto que parece com a string alvo.
# Se a função retornar 1, foi encontrado exatamente a string alvo dentro do texto (desconsidera letras maiusculas e espaços).
def avaliar_ocorrencia_de_string_em_lista_de_strings(linhas_de_texto, string):
    """Procura uma string em uma lista de strings e retorna um score de 0 a 1, onde 1 representa um match perfeito."""
    
    # Remove acentos, espaços, e transforma tudo em letra minuscula.
    string = tratar_string(string)
    max_ratio_geral = 0
    
    for linha in linhas_de_texto:
        # Remove acentos, espaços, e transforma tudo em letra minuscula.
        linha_tratada = tratar_string(linha)
        max_ratio_linha = 0
        
        # Trata o caso em que a linha de texto é menor que a string alvo
        if len(linha_tratada) < len(string):
            max_ratio_linha = SequenceMatcher(None, linha_tratada, string).ratio()
        else:
            # Percorre substrings dentro de cada linha de texto e compara com a string alvo
            for i in range(len(linha_tratada)-len(string)+1): 
                curr_string = linha_tratada[i:i+len(string)] 
                # Computa o "ratio", que corresponde a similariedade entre as strings (usando a biblioteca difflib)
                ratio = SequenceMatcher(None, curr_string, string).ratio()
                max_ratio_linha = ratio if ratio > max_ratio_linha else max_ratio_linha
        max_ratio_geral = max_ratio_linha if max_ratio_linha > max_ratio_geral else max_ratio_geral
    
    return max_ratio_geral


# Dado uma lista de strings e um texto (texto corrido ou linhas de texto), essa função rankea as strings por sua similariedade com trechos do texto
def rankear_strings_por_ocorrencia(lista_strings, texto, tipo='linhas'):
    """Ranqueia strings pelo seu 'score'. 'Score' alto significa que uma string parecida foi encontrada no texto.
       O texto pode ser um texto corrido (tipo = 'texto') ou em formato de linhas de texto (tipo = 'linhas').
    """
    lista_scores = []
    # Cria lista com o score de cada string
    for string in lista_strings:
        if tipo == 'linhas':
            score = avaliar_ocorrencia_de_string_em_lista_de_strings(texto,string)
        elif tipo == 'texto':
            score = avaliar_ocorrencia_de_string_em_texto(texto,string)
        else:
            raise Exception('''
            O parâmetro "tipo" deve ser "linhas" (caso o texto seja uma lista de strings)
            ou "texto" (caso seja uma string única).
            ''')
        lista_scores.append(score)
    
    # Cria um df com as strings e seus scores. Inclui o comprimento das strings, e ordena pelo score e comprimento.
    df = pd.DataFrame(list(zip(lista_strings, lista_scores)),columns=['string','score'])
    df['len_string'] = df['string'].apply(lambda x: len(x))
    df.sort_values(by=['score','len_string'],ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df


# Dado um dataframe com strings rankeadas, verifica se as strings com 'match' exato no texto são substrings
# de outras strings que também tiveram 'match' exato no texto.
def definir_strings_contidas_em_outras(df):
    """Verifica se strings estão contidas em outras strings."""
    new_df = df.copy()
    new_df['contida'] = 0
    
    lista_strings = list(new_df['string'][new_df['score']==1])
    lista_strings.reverse()
    
    # Para cada string, verificar se ela está contida nas outras strings
    for i in range(len(lista_strings)):
        string_atual = lista_strings[i]
        string_restantes = lista_strings[i+1:]
        matches = [s for s in string_restantes if string_atual in s]
        if len(matches) > 0:
            new_df.loc[df['string']==string_atual,'contida'] = 1
    return new_df

# Recebe um df com o score de cada string, e retorna a "melhor string".
def retornar_melhor_string(df):
    """Recebe um df com strings rankeadas, e retorna a melhor string, dado certas condições."""
    new_df = definir_strings_contidas_em_outras(df)
    # remove strings contidas em outras
    new_df = new_df[new_df['contida']==0]
    
    # Trata exceções.
    try:
        if new_df.iloc[1]['score'] > 0.95:
            # Caso onde aparece tanto "Careplus" quanto "Mediservice" na carteira - Considerar "Careplus"
            if new_df.iloc[1]['string'] == 'Careplus':
                return 'Careplus', new_df.iloc[1]['score']
            # ATENÇÃO!! As vezes aparece Mediservice e Omint e o certo é MediService - TRATAR!
            elif new_df.iloc[1]['string'] == 'Omint':
                return 'Omint', new_df.iloc[1]['score']
            elif new_df.iloc[0]['string'] == 'PREMIUM':
                return new_df.iloc[1]['string'], new_df.iloc[1]['score']
    except:
        pass  # Prática ruim - Melhorar código para capturar exceções
    
    resposta = new_df.iloc[0]['string']
    score = new_df.iloc[0]['score']
    return resposta, score
