import random
import time

# Função para gerar números de conta aleatórios
def gerar_numeros_conta(quantidade, inicio=10000, fim=99999):
    return [random.randint(inicio, fim) for _ in range(quantidade)]

# Função de hash usando os últimos três dígitos do número da conta
def funcao_hash(numero_conta):
    return (numero_conta % 1000) % 9

# Classe da tabela hash com Encadeamento Separado
class TabelaHashEncadeamento:
    def __init__(self, tamanho):
        self.tabela = [[] for _ in range(tamanho)]
        
    def inserir(self, numero_conta):
        chave = funcao_hash(numero_conta)
        self.tabela[chave].append(numero_conta)
        
    def buscar(self, numero_conta):
        chave = funcao_hash(numero_conta)
        if numero_conta in self.tabela[chave]:
            return True
        return False

# Classe da tabela hash com Sondagem Linear
class TabelaHashSondagemLinear:
    def __init__(self, tamanho):
        self.tabela = [None] * tamanho
        
    def inserir(self, numero_conta):
        chave = funcao_hash(numero_conta)
        inicio = chave
        while self.tabela[chave] is not None:
            chave = (chave + 1) % len(self.tabela)
            if chave == inicio:
                raise Exception("Tabela Hash está cheia")
        self.tabela[chave] = numero_conta
        
    def buscar(self, numero_conta):
        chave = funcao_hash(numero_conta)
        inicio = chave
        while self.tabela[chave] is not None:
            if self.tabela[chave] == numero_conta:
                return True
            chave = (chave + 1) % len(self.tabela)
            if chave == inicio:
                break
        return False

# Função para analisar a eficiência da tabela hash
def analisar_tabela_hash(tabela_hash_class, numeros_conta):
    tabela_hash = tabela_hash_class(100)  # Aumentar o tamanho da tabela para evitar lotação
    tempo_insercao = 0
    tempo_busca = 0
    
    print(f"Analisando {tabela_hash_class.__name__}...")
    for numero in numeros_conta:
        inicio = time.perf_counter()
        tabela_hash.inserir(numero)
        tempo_insercao += time.perf_counter() - inicio
    
    print(f"Total de inserções realizadas: {len(numeros_conta)}")
    
    for numero in numeros_conta:
        inicio = time.perf_counter()
        tabela_hash.buscar(numero)
        tempo_busca += time.perf_counter() - inicio
    
    return tempo_insercao, tempo_busca

# Gerar números de conta
numeros_conta = gerar_numeros_conta(1000)

# Analisar Encadeamento Separado
try:
    tempo_insercao_encadeamento, tempo_busca_encadeamento = analisar_tabela_hash(TabelaHashEncadeamento, numeros_conta)
    print(f"Encadeamento Separado - Tempo de Inserção: {tempo_insercao_encadeamento:.6f} segundos, Tempo de Busca: {tempo_busca_encadeamento:.6f} segundos")
except Exception as e:
    print(f"Erro durante a análise com Encadeamento Separado: {e}")

# Analisar Sondagem Linear
try:
    tempo_insercao_sondagem, tempo_busca_sondagem = analisar_tabela_hash(TabelaHashSondagemLinear, numeros_conta)
    print(f"Sondagem Linear - Tempo de Inserção: {tempo_insercao_sondagem:.6f} segundos, Tempo de Busca: {tempo_busca_sondagem:.6f} segundos")
except Exception as e:
    print(f"Erro durante a análise com Sondagem Linear: {e}")
