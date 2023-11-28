# -*- coding: utf-8 -*-

# Importa bibliotecas.
from flask import Flask, jsonify, request, abort, make_response, json, Response
import sqlite3

# Cria aplicativo Flask.
app = Flask(__name__)

# Configura o character set das transações HTTP para UTF-8.
json.provider.DefaultJSONProvider.ensure_ascii = False

# Especifica a base de dados SQLite3.
database = "./teste-db.db"


def prefix_remove(prefix, data):

    # Função que remove os prefixos dos nomes dos campos de um 'dict'.
    # Por exemplo, prefix_remove('item_', { 'item_id': 2, 'item_name': 'Coisa', 'item_status': 'on' })
    # retorna { 'id': 2, 'name': 'Coisa', 'status': 'on' }
    # Créditos: Comunidade StackOverflow.

    new_data = {}
    for key, value in data.items():
        if key.startswith(prefix):
            new_key = key[len(prefix):]
            new_data[new_key] = value
        else:
            new_data[key] = value
    return new_data


@app.route("/items", methods=["GET"])
def get_all():

    # Obtém todos os registros válidos de 'item'.
    # Request method → GET
    # Request endpoint → /items
    # Response → JSON

    try:

        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)

        # Formata os dados retornados na factory como SQLite.Row.
        conn.row_factory = sqlite3.Row

        # Cria um cursor de dados.
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute(
            "SELECT * FROM item WHERE item_status = 'on' ORDER BY item_date DESC")

        # Retorna todos os resultados da consulta para 'items_rows'.
        items_rows = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        conn.close()

        # Cria uma lista para armazenar os registros.
        items = []

        # Converte cada SQLite.Row em um dicionário e adiciona à lista 'registros'.
        for item in items_rows:
            items.append(dict(item))

        # Verifica se há registros antes de retornar...
        if items:

            # Remove prefixos dos campos.
            new_items = [prefix_remove('item_', item) for item in items]

            # Se houver registros, retorna tudo.
            return new_items, 200
        else:
            # Se não houver registros, retorna erro.
            return {"error": "Nenhum item encontrado"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as error:  # Outros erros.
        return {"error": f"Erro inesperado: {str(error)}"}, 500


@app.route("/items/<int:id>", methods=["GET"])
def get_one(id):

    # Obtém um registro único de 'item', identificado pelo 'id'.
    # Request method → GET
    # Request endpoint → /items/<id>
    # Response → JSON

    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute(
            "SELECT * FROM item WHERE item_id = ? AND item_status = 'on'", (id,))

        # Retorna o resultado da consulta para 'item_row'.
        item_row = cursor.fetchone()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Se o registro existe...
        if item_row:

            # Converte SQLite.Row para dicionário e armazena em 'item'.
            item = dict(item_row)

            # Remove prefixos dos campos.
            new_item = prefix_remove('item_', item)

            # Retorna item.
            return new_item, 200
        else:
            # Se não encontrar o registro, retorna erro.
            return {"error": "Item não encontrado"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as error:  # Outros erros.
        return {"error": f"Erro inesperado: {str(error)}"}, 500


@app.route('/items', methods=["POST"])
def create():

    # Cadastra um novo registro em 'item'.
    # Request method → POST
    # Request endpoint → /items
    # Request body → JSON (raw) → { String:name, String:description, String:location, int:owner }
    # Response → JSON → { "success": "Registro criado com sucesso", "id": id do novo registro }}

    try:
        # Recebe dados do body da requisição na forma de 'dict'.
        new_item = request.get_json()

        # Conecta ao banco de dados.
        # Observe que 'row_factory' é desnecessário porque não receberemos dados do banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Query que insere um novo registro na tabela 'item'.
        sql = "INSERT INTO item (item_name, item_description, item_location, item_owner) VALUES (?, ?, ?, ?)"

        # Dados a serem inseridos, obtidos do request.
        sql_data = (
            new_item['name'],
            new_item['description'],
            new_item['location'],
            new_item['owner']
        )

        # Executa a query, fazendo as devidas substituições dos curingas (?) pelos dados (sql_data).
        cursor.execute(sql, sql_data)

        # Obter o ID da última inserção
        inserted_id = int(cursor.lastrowid)

        # Salvar as alterações no banco de dados.
        conn.commit()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Retorna com mensagem de sucesso e status HTTP "201 Created".
        return {"success": "Registro criado com sucesso", "id": inserted_id}, 201

    except json.JSONDecodeError as e:  # Erro ao obter dados do JSON.
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}, 500

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as error:  # Outros erros.
        return {"error": f"Erro inesperado: {str(error)}"}, 500


@app.route("/items/<int:id>", methods=["PUT", "PATCH"])
def edit(id):

    # Edita um registro em 'item', identificado pelo 'id'.
    # Request method → PUT ou PATCH
    # Request endpoint → /items/<id>
    # Request body → JSON (raw) → { String:name, String:description, String:location, int:owner }
    #       OBS: usando "PATCH", não é necessário enviar todos os campos, apenas os que serão alterados.
    # Response → JSON → { "success": "Registro atualizado com sucesso", "id": id do registro }
    try:
        # Recebe os dados do corpo da requisição.
        item_json = request.get_json()
        
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query ára atualizar o banco de dados.
        # Query que pesquisa a existência do registro.
        sql = "SELECT item_id FROM item WHERE item_id = ? AND item_status != 'off'"
        
        # Executa a query.
        cursor.execute(sql, (id,))
        
        # Retorna o resultado da consulta para 'item_row'.
        item_row = cursor.fetchone()
        
        
        if item_row:
            
            # Loop para atualizar os campos específicos do registro na tabela 'item'.
            # Observe que o prefixo 'item_' é adicionado ao(s) nome(s) do(s) campo(s).
            set_clause = ', '.join([f"item_{key} = ?" for key in item_json.keys()])

            # Monta SQL com base nos campos a serem atualizados.
            sql = f"UPDATE item SET {set_clause} WHERE item_id = ? AND item_status = 'on'"
            cursor.execute(sql, (*item_json.values(), id))
        # Commit para salvar as alterações.
            conn.commit()

            # Fechar a conexão com o banco de dados.
            conn.close()

            #    Retorna com mensagem de sucesso e status HTTP "200 Ok".
            return {"success": "Registro atualizado com sucesso", "id": id}, 200
        else:
            # fecha o banco de dados.
            conn.close()
            
            # Se não encontrar o registro, retorna erro.
            return {"error": "Item não encontrado"}, 404
        
    except json.JSONDecodeError as e:  # Erro ao obter dados do JSON.
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}, 500
    
    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/items/<int:id>", methods=["DELETE"])
def delete_items(id):

    # Marca, como apagado, um registro único de 'item', identificado pelo 'id'.
    # Request method → DELETE
    # Request endpoint → /items/<id>
    # Response → JSON → { "success": "Registro apagado com sucesso", "id": id do registro }

    try: 
        # Conecta ao banco de dados.
        # Observe que 'row_factory' é desnecessário porque não receberemos dados do banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        conn.row_factory = sqlite3.Row
        
        # Query ára atualizar o banco de dados.
        # Query que pesquisa a existência do registro.
        sql = "SELECT item_id FROM item WHERE item_id = ? AND item_status != 'off'"
        
        # Executa a query.
        cursor.execute(sql, (id,))
        
        # Retorna o resultado da consulta para 'item_row'.
        item_row = cursor.fetchone()


        if item_row:
            
            sql = "UPDATE item SET item_status = 'off' WHERE item_id = ?"

            # executa a Query.
            cursor.execute(sql, (id,))
            # Salvar no banco de dados.
            conn.commit()
        
            # fechar banco de dados.
            conn.close()

            #    Retorna com mensagem de sucesso e status HTTP "200 Ok".
            return {"success": "Registro apagado com sucesso", "id": id}, 200
        else:
            # fecha o banco de dados.
            conn.close()
            
            # Se não encontrar o registro, retorna erro.
            return {"error": "Item não encontrado"}, 404
        

    
    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as error:  # Outros erros.
        return {"error": f"Erro inesperado: {str(error)}"}, 500

@app.route("/owners", methods=["GET"])
def get_owner_all():
    try:
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        sql = "SELECT * FROM owner ORDER BY owner_name"
        cursor.execute(sql)
        owners_rows = cursor.fetchall()
        conn.close()
        
        owners = []
        
        for owner in owners_rows:
            owners.append(dict(owner))
        
        if owners:

            # Remove prefixos dos campos.
            new_owners = [prefix_remove('owner_', owner) for owner in owners]

            # Se houver registros, retorna tudo.
            return new_owners, 200
        else:
            # Se não houver registros, retorna erro.
            return {"error": "Nenhum proprietário encontrado"}, 404
    
    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as error:  # Outros erros.
        return {"error": f"Erro inesperado: {str(error)}"}, 500
    
@app.route("/owners/<int:id>", methods=["GET"])
def get_owner_id(id):
    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute(
            "SELECT * FROM owner WHERE owner_id = ? AND owner_status = 'on'", (id,))

        # Retorna o resultado da consulta para 'item_row'.
        owners_row = cursor.fetchone()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Se o registro existe...
        if owners_row:

            # Converte SQLite.Row para dicionário e armazena em 'item'.
            owner = dict(owners_row)

            # Remove prefixos dos campos.
            new_owner = prefix_remove('owner_', owner)

            # Retorna item.
            return new_owner, 200
        else:
            # Se não encontrar o registro, retorna erro.
            return {"error": "Proprietário não encontrado"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as error:  # Outros erros.
        return {"error": f"Erro inesperado: {str(error)}"}, 500
    
@app.route('/owners', methods=["POST"])
def create_new_owner():

    # Cadastra um novo registro em 'item'.
    # Request method → POST
    # Request endpoint → /items
    # Request body → JSON (raw) → { String:name, String:description, String:location, int:owner }
    # Response → JSON → { "success": "Registro criado com sucesso", "id": id do novo registro }}

    try:
        # Recebe dados do body da requisição na forma de 'dict'.
        new_owner = request.get_json()

        # Conecta ao banco de dados.
        # Observe que 'row_factory' é desnecessário porque não receberemos dados do banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Query que insere um novo registro na tabela 'item'.
        sql = "INSERT INTO owner (owner_name, owner_email, owner_password, owner_birth) VALUES (?, ?, ?, ?)"

        # Dados a serem inseridos, obtidos do request.
        sql_data = (
            new_owner['name'],
            new_owner['email'],
            new_owner['password'],
            new_owner['birth']
        )

        # Executa a query, fazendo as devidas substituições dos curingas (?) pelos dados (sql_data).
        cursor.execute(sql, sql_data)

        # Obter o ID da última inserção
        inserted_id = int(cursor.lastrowid)

        # Salvar as alterações no banco de dados.
        conn.commit()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Retorna com mensagem de sucesso e status HTTP "201 Created".
        return {"success": "Registro criado com sucesso", "id": inserted_id}, 201


    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as error:  # Outros erros.
        return {"error": f"Erro inesperado: {str(error)}"}, 500

@app.route("/owners/<int:id>", methods=["PUT", "PATCH"])
def edit_owners(id):

    # Edita um registro em 'item', identificado pelo 'id'.
    # Request method → PUT ou PATCH
    # Request endpoint → /items/<id>
    # Request body → JSON (raw) → { String:name, String:description, String:location, int:owner }
    #       OBS: usando "PATCH", não é necessário enviar todos os campos, apenas os que serão alterados.
    # Response → JSON → { "success": "Registro atualizado com sucesso", "id": id do registro }
    try:
        # Recebe os dados do corpo da requisição.
        owner_json = request.get_json()
        
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query ára atualizar o banco de dados.
        # Query que pesquisa a existência do registro.
        sql = "SELECT owner_id FROM owner WHERE owner_id = ? AND owner_status != 'off'"
        
        # Executa a query.
        cursor.execute(sql, (id,))
        
        # Retorna o resultado da consulta para 'item_row'.
        owner_row = cursor.fetchone()
        
        
        if owner_row:
            
            # Loop para atualizar os campos específicos do registro na tabela 'item'.
            # Observe que o prefixo 'item_' é adicionado ao(s) nome(s) do(s) campo(s).
            set_clause = ', '.join([f"owner_{key} = ?" for key in owner_json.keys()])

            # Monta SQL com base nos campos a serem atualizados.
            sql = f"UPDATE owner SET {set_clause} WHERE owner_id = ? AND owner_status = 'on'"
            cursor.execute(sql, (*owner_json.values(), id))
        # Commit para salvar as alterações.
            conn.commit()

            # Fechar a conexão com o banco de dados.
            conn.close()

            #    Retorna com mensagem de sucesso e status HTTP "200 Ok".
            return {"success": "Registro atualizado com sucesso", "id": id}, 200
        else:
            # fecha o banco de dados.
            conn.close()
            
            # Se não encontrar o registro, retorna erro.
            return {"error": "Proprietário não encontrado"}, 404
        
    except json.JSONDecodeError as e:  # Erro ao obter dados do JSON.
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}, 500
    
    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500

@app.route("/owners/<int:id>", methods=["DELETE"])
def delete(id):

    # Marca, como apagado, um registro único de 'item', identificado pelo 'id'.
    # Request method → DELETE
    # Request endpoint → /items/<id>
    # Response → JSON → { "success": "Registro apagado com sucesso", "id": id do registro }

    try: 
        # Conecta ao banco de dados.
        # Observe que 'row_factory' é desnecessário porque não receberemos dados do banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        conn.row_factory = sqlite3.Row
        
        # Query ára atualizar o banco de dados.
        # Query que pesquisa a existência do registro.
        sql = "SELECT owner_id FROM owner WHERE owner_id = ? AND owner_status != 'off'"
        
        # Executa a query.
        cursor.execute(sql, (id,))
        
        # Retorna o resultado da consulta para 'item_row'.
        owner_row = cursor.fetchone()


        if owner_row:
            
            sql = "UPDATE owner SET owner_status = 'off' WHERE owner_id = ?"

            # executa a Query.
            cursor.execute(sql, (id,))
            # Salvar no banco de dados.
            conn.commit()
        
            # fechar banco de dados.
            conn.close()

            #    Retorna com mensagem de sucesso e status HTTP "200 Ok".
            return {"success": "Registro apagado com sucesso", "id": id}, 200
        else:
            # fecha o banco de dados.
            conn.close()
            
            # Se não encontrar o registro, retorna erro.
            return {"error": "Item não encontrado"}, 404
        

    
    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as error:  # Outros erros.
        return {"error": f"Erro inesperado: {str(error)}"}, 500

# achar um item cadastrado por 1 porprietario
@app.route("/owners/item/<int:id>", methods=["GET"])
def get_item_owner(id):
    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute(
            "SELECT * FROM item WHERE item_owner = ?", (id,))

        # Retorna o resultado da consulta para 'item_row'.
        owners_items_row = cursor.fetchall()
        owners_items = []
        
        for owner in owners_items_row:
            owners_items.append(dict(owner))

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Se o registro existe...
        if owners_items:

            new_owner_items = owners_items

            # Retorna item.
            return new_owner_items, 200
        else:
            # Se não encontrar o registro, retorna erro.
            return {"error": "Proprietário não contém items cadastrados"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as error:  # Outros erros.
        return {"error": f"Erro inesperado: {str(error)}"}, 500
        
@app.route("/owners/items/<int:id>", methods=["GET"])
def owner_and_id(id):
        # Conecta ao banco de dados.
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Execute SQL
        cursor.execute("""
            SELECT item.*, owner.* 
            FROM item 
            INNER JOIN owner ON item.item_owner = owner.owner_id 
            WHERE item.item_id = ?
        """, (id,))

        # Fetch all rows
        owners_items_row = cursor.fetchall()
        owners_items = []

        for row in owners_items_row:
            owners_items.append(dict(row))

        # Close the connection
        conn.close()

        # If records exist...
        if owners_items:
            # Extract item and owner data into separate lists
            item_list = [item['item_name'] for item in owners_items]
            owner_list = [owner['owner_name'] for owner in owners_items]

            # Return item and owner lists
            return {"items": item_list, "owners": owner_list}, 200
        else:
            # If no records found, return an error
            return {"error": "Proprietário não contém items cadastrados"}, 404

    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as error:
        return {"error": f"Erro inesperado: {str(error)}"}, 500

@app.route("/items/search/<query>", methods=["GET"])
def get_search(query):
    try:
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM item WHERE item_status != 'off' AND (
            item_name LIKE '%'||?||'%' OR
            item_description LIKE '%'||?||'%' OR
            item_location LIKE '%'||?||'%'
            );
        """, (query, query, query,))
        search_query = cursor.fetchall()
        conn.close()
        
        querys = []
        
        for item_search in search_query:
            querys.append(dict(item_search))
        
        if querys:

            # Remove prefixos dos campos.
            new_search = [prefix_remove('item_', item_search) for item_search in querys]

            # Se houver registros, retorna tudo.
            return new_search, 200
        else:
            # Se não houver registros, retorna erro.
            return {"error": "Nenhum resultado encontrado"}, 404
    
    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as error:  # Outros erros.
        return {"error": f"Erro inesperado: {str(error)}"}, 500

@app.route("/contacts", methods=["POST"])
def contacts():

    # Cadastra um novo contato em 'contact'.
    # Request method → POST
    # Request endpoint → /contacts
    # Request body → JSON (raw) → { string:name, string:email, string:subject, string:message }
    # Response → JSON → { "success": "Registro criado com sucesso", "id": id do novo registro }

    try:
        new_item = request.get_json()
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        sql = "INSERT INTO contact (name, email, subject, message) VALUES (?, ?, ?, ?)"
        sql_data = (
            new_item['name'],
            new_item['email'],
            new_item['subject'],
            new_item['message']
        )
        cursor.execute(sql, sql_data)
        inserted_id = int(cursor.lastrowid)
        conn.commit()
        conn.close()

        if inserted_id > 0:
            return {"success": "Contato enviado com sucesso", "id": inserted_id, "name": new_item['name']}, 201

    except json.JSONDecodeError as e:
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}, 500
    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500


# Roda aplicativo Flask.
if __name__ == "__main__":
    app.run(debug=True)