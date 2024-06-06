import random
import time
import pandas as pd
import string

# Função para gerar números de conta aleatórios
def gerar_numeros_conta(quantidade, inicio=10000, fim=99999):
    return [random.randint(inicio, fim) for _ in range(quantidade)]

# Função de hash usando os últimos três dígitos do número da conta
def funcao_hash(numero_conta):
    return (numero_conta % 1000) % 9 

# Função para gerar nomes aleatórios
def gerar_nome():
    return ''.join(random.choices(string.ascii_uppercase, k=5))

# Classe da tabela hash com Encadeamento Separado
class TabelaHashEncadeamento:
    def __init__(self, tamanho):
        self.tabela = [[] for _ in range(tamanho)]
        
    def inserir(self, numero_conta, nome_cliente):
        chave = funcao_hash(numero_conta)
        self.tabela[chave].append((numero_conta, nome_cliente))
        
    def buscar(self, numero_conta):
        chave = funcao_hash(numero_conta)
        for conta, nome in self.tabela[chave]:
            if conta == numero_conta:
                return True
        return False

# Classe da tabela hash com Sondagem Linear
class TabelaHashSondagemLinear:
    def __init__(self, tamanho):
        self.tabela = [None] * tamanho
        
    def inserir(self, numero_conta, nome_cliente):
        chave = funcao_hash(numero_conta)
        while self.tabela[chave] is not None:
            chave = (chave + 1) % len(self.tabela)
        self.tabela[chave] = (numero_conta, nome_cliente)
        
    def buscar(self, numero_conta):
        chave = funcao_hash(numero_conta)
        while self.tabela[chave] is not None:
            if self.tabela[chave][0] == numero_conta:
                return True
            chave = (chave + 1) % len(self.tabela)
        return False

# Função para analisar a eficiência da tabela hash
def analisar_tabela_hash(tabela_hash_class, numeros_conta, nomes_clientes, tamanho_tabela):
    tabela_hash = tabela_hash_class(tamanho_tabela)
    tempo_insercao = 0
    tempo_busca = 0
    
    print(f"Analisando {tabela_hash_class.__name__} com tamanho {tamanho_tabela}...")
    for numero, nome in zip(numeros_conta, nomes_clientes):
        inicio = time.perf_counter()
        tabela_hash.inserir(numero, nome)
        tempo_insercao += time.perf_counter() - inicio
    
    print(f"Total de inserções realizadas: {len(numeros_conta)}")
    
    for numero in numeros_conta:
        inicio = time.perf_counter()
        tabela_hash.buscar(numero)
        tempo_busca += time.perf_counter() - inicio
    
    return tempo_insercao, tempo_busca, tabela_hash.tabela

# Gerar números de conta e nomes de clientes
numeros_conta = gerar_numeros_conta(1000)
nomes_clientes = [gerar_nome() for _ in range(1000)]

# Tamanho da tabela
tamanho_tabela = 2000

# Analisar Encadeamento Separado
resultados = []
try:
    tempo_insercao_encadeamento, tempo_busca_encadeamento, tabela_encadeamento = analisar_tabela_hash(TabelaHashEncadeamento, numeros_conta, nomes_clientes, tamanho_tabela)
    print(f"Encadeamento Separado - Tempo de Inserção: {tempo_insercao_encadeamento:.6f} segundos, Tempo de Busca: {tempo_busca_encadeamento:.6f} segundos")
    resultados.append(['Encadeamento Separado', 'Inserção', tempo_insercao_encadeamento])
    resultados.append(['Encadeamento Separado', 'Busca', tempo_busca_encadeamento])
except Exception as e:
    print(f"Erro durante a análise com Encadeamento Separado: {e}")

# Analisar Sondagem Linear
try:
    tempo_insercao_sondagem, tempo_busca_sondagem, tabela_sondagem = analisar_tabela_hash(TabelaHashSondagemLinear, numeros_conta, nomes_clientes, tamanho_tabela)
    print(f"Sondagem Linear - Tempo de Inserção: {tempo_insercao_sondagem:.6f} segundos, Tempo de Busca: {tempo_busca_sondagem:.6f} segundos")
    resultados.append(['Sondagem Linear', 'Inserção', tempo_insercao_sondagem])
    resultados.append(['Sondagem Linear', 'Busca', tempo_busca_sondagem])
except Exception as e:
    print(f"Erro durante a análise com Sondagem Linear: {e}")

# Criar DataFrame com os resultados
df_resultados = pd.DataFrame(resultados, columns=['Método', 'Operação', 'Tempo (segundos)'])

# Criar DataFrames com as tabelas hash
df_tabela_encadeamento = pd.DataFrame([(i, entrada) for i, entrada in enumerate(tabela_encadeamento)], columns=['Posição', 'Entradas'])
df_tabela_sondagem = pd.DataFrame([(i, entrada) for i, entrada in enumerate(tabela_sondagem)], columns=['Posição', 'Entradas'])

# Salvar os resultados em um arquivo Excel
with pd.ExcelWriter('resultados_tabela_hash.xlsx') as writer:
    df_resultados.to_excel(writer, sheet_name='Resultados', index=False)
    df_tabela_encadeamento.to_excel(writer, sheet_name='Encadeamento Separado', index=False)
    df_tabela_sondagem.to_excel(writer, sheet_name='Sondagem Linear', index=False)