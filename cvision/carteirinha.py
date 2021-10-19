from cvision.cloud_vision import conectar_cloud_vision_e_detectar_texto, extrair_texto_cloud_vision
from cvision.utils import listar_todas_operadoras, listar_planos_de_operadora, tratar_string
from cvision.comparacao_strings import rankear_strings_por_ocorrencia, retornar_melhor_string
import regex as re

class CarteirinhaSaude:
    def __init__(self, path, df_operadoras_planos, origem='s3', bucket_name='beep-production'):
        self.path_to_file = path
        self.df_operadoras_planos = df_operadoras_planos
        self.bucket_name = bucket_name
        self.texto_detectado = None
        self.texto_extraido = None
        self.linhas_de_texto = None
        self.df_operadoras = None
        self.df_planos = None
        self.operadora = None
        self.score_operadora = None
        self.plano = None
        self.id_plano = None
        self.score_plano = None
        self.num_carteirinha = None
        self.origem = origem
        self.dict_operadora_num_chars = {
                                        'Amil': 9,
                                        'Amil One': 9,
                                        'Bradesco' : 15,
                                        'Careplus' : 12,
                                        'Fapes' : 8,
                                        'MediService' : 18,
                                        'Omint' : 13
                                    }
        
    def detectar_texto(self):
        self.texto_detectado = conectar_cloud_vision_e_detectar_texto(self.path_to_file, origem=self.origem, bucket_name=self.bucket_name)
        
    def extrair_texto(self):
        self.texto_extraido = extrair_texto_cloud_vision(self.texto_detectado)
        self.linhas_de_texto = self.texto_extraido.split('\n')
        
    def rankear_operadoras(self):
        lista_operadoras = listar_todas_operadoras(self.df_operadoras_planos)
        self.df_operadoras = rankear_strings_por_ocorrencia(lista_operadoras, self.texto_extraido, tipo='texto')
        
    def extrair_operadora(self):
        self.operadora, self.score_operadora = retornar_melhor_string(self.df_operadoras)
        
    def rankear_planos(self):
        lista_planos = listar_planos_de_operadora(self.operadora, self.df_operadoras_planos)
        self.df_planos = rankear_strings_por_ocorrencia(lista_planos, self.linhas_de_texto, tipo='linhas')
        
    def extrair_plano(self):
        if self.score_operadora > 0.8:  # Só procurar por planos caso o score da operadora tenha sido alto (> 0.8)
            self.plano, self.score_plano = retornar_melhor_string(self.df_planos)
            cols = ['operadora', 'string_alvo']
            valores = [self.operadora, self.plano]
            self.id_plano = self.df_operadoras_planos[(self.df_operadoras_planos[cols] == valores).all(1)].id_plano.values[0]
            
            if self.score_plano < 0.8:
                self.plano, self.id_plano = None, None
        
        
    def extrair_num_carteirinha(self):
        
        resultados = []
        num_chars_carteirinha = self.dict_operadora_num_chars[self.operadora]

        # Cria pattern do Regex de acordo com o num de digitos de cada plano
        string = r"^[\d]{" + str(num_chars_carteirinha) + "}$"
        pattern = re.compile(string)

        # Procura todas as sequencias numericas com o comprimento (num_char) esperado.
        # Olha apenas numeros que estao em sequencia na imagem (na mesma linha)
        for txt in self.linhas_de_texto:
            matches = re.findall(pattern, tratar_string(txt), overlapped=True)
            if len(matches)>0:
                for match in matches:
                    resultados.append(match)

        # No caso que o plano é Rede Nacional, os números as vezes ficam muito separado na carteira,
        # e o OCR detecta como linhas de texto diferentes. Nesse caso, procurar também um .                
        if len(resultados) < 1 and (self.plano == 'REDE NACIONAL' or self.plano == 'NACIONAL FLEX' or self.plano == 'NACIONAL PLUS'):
            pattern  = re.compile(r"[1-9][\d]{14}[^0-9]*")
            texto_completo = self.texto_extraido
            # Trocar "O" por "0" para tratar os casos recorrentes em que o algoritimo identifica erradamente
            texto_completo = texto_completo.replace('O','0')
            matches = re.findall(pattern, tratar_string(texto_completo), overlapped=True)
            if len(matches)>0:
                for match in matches:
                    apenas_digitos = re.sub("[^0-9]", "", match)
                    resultados.append(apenas_digitos)

        # Trata o fato de que existe um número de 9 dígitos no verso da carteirinha Amil One que não é o núm. do plano.
        # A solução é só retornar um resultado se a foto for da frente da carteirinha (verificar pelo score_plano).
        if self.operadora == 'Amil One' and self.score_plano < 0.9:
            resultados = []

        # Se mais de um número foi encontrado pelo Regex, retorna o último número encontrado
        # (mais provavel de estar certo de acordo com as análises realizadas)
        if len(resultados) > 0:  
            self.num_carteirinha = resultados[-1]
        

    def extrair_operadora_plano_num_carteirinha(self):
        self.detectar_texto()
        self.extrair_texto()
        self.rankear_operadoras()
        self.extrair_operadora()
        self.rankear_planos()
        self.extrair_plano()
        self.extrair_num_carteirinha()
        
        if self.score_operadora < 0.95:
            self.operadora
        
    def infos(self):
        print(f'Operadora: {self.operadora} ----- Score: {self.score_operadora}')
        print(f'Plano: {self.plano} ----- Score: {self.score_plano}')
        print(f'Núm. Carteirinha: {self.num_carteirinha}')