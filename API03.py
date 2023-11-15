# -*- coding: utf-8 -*-

# Importa as bilbiotecas de dependências.
import json
import sqlite3
import os

# Define o banco de dados.
database = './teste-db.db'

# Obtém todos os 'item' válidos do banco de dados.
# Retorna como uma 'list' de 'dict'.


def get_all_items():

    # Cria uma conexão com o banco de dados SQLite.
    conn = sqlite3.connect(database)

    # Define que a troca de dados entre Python e SQLite acontece na for a de Row.
    conn.row_factory = sqlite3.Row

    # Um cursor que aponta para a(s) linha(s) do SQLite.Row que está(ão) sendo acessadas.
    cursor = conn.cursor()

    # Query para consultar os registrosn na tabela 'item'.
    sql = "SELECT * FROM item WHERE item_status != 'off'"

    # Executa o SQL acima no banco de dados.
    cursor.execute(sql)

    # "Puxa" os dados do cursor para o Python.
    data = cursor.fetchall()

    # Desconecta do banco de dados.
    # Guarda recursos, aumenta a segurança, evita corrupção de dados.
    conn.close()

    # Uma 'list' para armazenar as SQLite.Row no forma de 'dict'.
    res = []

    # Loop que obtém cada SLite.Row da memória (data).
    for res_temp in data:

        # Converte a SQLite.Row em 'dict' e adiciona no final de 'res' (list).
        res.append(dict(res_temp))

    # Devolve os dados processados para quem solicitou.
    return res

def get_one_item(id):
    # Inicializa o banco de dados.
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Query consulta.
    sql = 'SELECT * FROM item WHERE item_status != "off" AND item_id = ?'
    
    #executar o código, porém passando o valor do ID.
    cursor.execute(sql, (id,))
    
    # Retorna o resultado da busca para 'data'.
    data = cursor.fetchone()
    
    # Fecha a conexão com o banco de daos.
    conn.close()
    
    # Se o registro existir...
    if data:
    
        # Retorna o registro em um 'dict'.
        return dict(data)
    
    else: # Se o registreno não chegou...
    
        # Retorna erro.
        return {'error': 'Registro não encontrado.'}
    
    

# Limpa o console.
os.system('cls')

# print( # Exibe no console.
#     json.dumps( # no formato JSON.
#         get_all_items(), # Items obtidos da função.
#         ensure_ascii=False, # Usando a tabela UTF-8.
#         indent=2 # Formata o JSON bunitim.
#     )
# )

print(json.dumps(get_one_item(3), ensure_ascii=False, indent=2))