import pandas as pd
import numpy as np

import logging

def limpar_valores_monetarios(valor):
    sufixo = valor[-1]
    if sufixo == "M":
        valor = float(valor[1:-1]) * 1000000
    elif sufixo == "K":
        valor = float(valor[1:-1]) * 1000
    else:
        return np.nan
    
    return int(valor)
    
def limpar_df_bruto(df):
    assert df.isnull().sum().all() == 0, "Há dados ausentes"
    assert df['link'].nunique() == len(df), "Dados duplicados"
    #-----------------
    #criar player_id
    #-----------------
    df['player_id'] = df['link'].apply(lambda x: x.split('/')[4])
    assert df['player_id'].nunique() == len(df), "ID do jogador não é único"
    #-----------------
    #criar country_id
    #-----------------
    df['country_id'] = df['country_link'].apply(lambda x: x.split('=')[-1])

    #-----------------
    #limpar colunas de valor e salário
    #-----------------
    df['valor_limpo'] = df['value'].apply(limpar_valores_monetarios)
    df['salario_limpo'] = df['wage'].apply(limpar_valores_monetarios)

    #imput dos valores com a média para aquela classificação geral
    df['valor_limpo'] = df.groupby('overall_rating')['valor_limpo'].transform(lambda x: x.fillna(x.mean()))
    df['salario_limpo'] = df.groupby('overall_rating')['salario_limpo'].transform(lambda x: x.fillna(x.mean()))

    #se ainda houver nan, substituir por 0 (estes tendem a ser jogadores de classificação muito baixa)
    df[['valor_limpo', 'salario_limpo']] = df[['valor_limpo', 'salario_limpo']].fillna(0)

    #-----------------
    #Reordenar colunas para o dataframe final
    #-----------------
    colunas_manter = ['player_id', 'name', 'age', 'overall_rating', 'potential',
                      'likes', 'dislikes', 'followers', 'valor_limpo', 'salario_limpo']

    ATRIBUTOS = ['Crossing', 'Finishing', 'Heading Accuracy', 'Short Passing', 'Volleys',
                 'Dribbling', 'Curve', 'FK Accuracy', 'Long Passing', 'Ball Control', 'Acceleration',
                 'Sprint Speed', 'Agility', 'Reactions', 'Balance', 'Shot Power', 'Jumping', 'Stamina',
                 'Strength', 'Long Shots', 'Aggression', 'Interceptions', 'Positioning', 'Vision',
                 'Penalties', 'Composure', 'Marking', 'Standing Tackle', 'Sliding Tackle', 'GK Diving',
                 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes']

    df_final = df[colunas_manter + ATRIBUTOS]
    assert df_final.isnull().sum().all() == 0

    return df_final

def unir_dados_posicoes(df):
    kaggle_df = pd.read_csv("0. raw/kaggle_data.csv")
    kaggle_df = kaggle_df[['ID', 'Position']]
    
    df['player_id'] = df['player_id'].astype('int64')
    
    df_unido = df.merge(kaggle_df, how='inner',
                        left_on=['player_id'],
                        right_on=['ID'])
    
    del df_unido['ID']
    
    return df_unido

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

    df = pd.read_csv("0. raw/data.csv")

    logging.info('Limpando dados...')

    df_limpo = limpar_df_bruto(df)

    logging.info('Limpeza do dataframe concluída')
    
    df_final = unir_dados_posicoes(df_limpo)
    
    logging.info('União do dataframe concluída')

    #salvar na pasta de dados processados
    pd.DataFrame(df_final).to_csv("1. processed/data_clean.csv", index=False, encoding='utf-8-sig')
    
    logging.info("Arquivo salvo com sucesso na pasta 'processed'")
