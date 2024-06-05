def contar_dados():
    """Compara o número de links armazenados e o número de linhas no banco de dados csv"""
    
    links = open('links_collected.txt').read().split('\n')
    links = [l for l in links if l != '']
    num_links = len(links)

    dados = open('data.csv', 'r', encoding='utf-8-sig').read()
    dados = dados.split('\n')[:-1]
    num_dados = len(dados) - 1

    print(f"links explorados\t\t:\t{num_links}")
    print(f"pontos de dados coletados\t:\t{num_dados}")
    print(f"\npontos de dados faltando\t:\t{num_links-num_dados}")

if __name__ == '__main__':
    contar_dados()
