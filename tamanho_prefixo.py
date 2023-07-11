import csv

def verificar_tamanho_prefixo(prefixo):
    endereco, mascara = prefixo.split("/")
    if "." in endereco:  # Prefixo IPv4
        tamanho_esperado = 32
    else:  # Prefixo IPv6
        tamanho_esperado = 128
    return int(mascara) <= tamanho_esperado

# Nome do arquivo CSV
nome_arquivo = "rrc15_tabela_roteamento_completa.csv"

# Nome da coluna que contem os prefixos
nome_coluna_prefixos = "Prefixo"

# Lista para armazenar os prefixos inconformes
prefixos_inconformes = []

# Leitura do arquivo CSV
with open(nome_arquivo, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        prefixo = row[nome_coluna_prefixos]
        if not verificar_tamanho_prefixo(prefixo):
            prefixos_inconformes.append(prefixo)

# Verificacao de conformidade de tamanho dos prefixos
if len(prefixos_inconformes) == 0:
    print("Todos os prefixos tem tamanho esperado.")
else:
    print("Prefixos com tamanho invalido encontrados. Salvando em arquivo.")

    # Nome do arquivo para salvar os prefixos inconformes
    nome_arquivo_inconformes = "prefixos_inconformes.txt"

    # Salvando os prefixos inconformes em um arquivo
    with open(nome_arquivo_inconformes, "w") as arquivo_inconformes:
        for prefixo in prefixos_inconformes:
            arquivo_inconformes.write(prefixo + "\n")

    print("Prefixos inconformes salvos em", nome_arquivo_inconformes)
