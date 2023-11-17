import json
import sqlite3
import os

database = './teste-db.db'

def get_owner_all():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM owner WHERE owner_status != 'off'"
    
    cursor.execute(sql)
    data_owner = cursor.fetchall()
    
    conn.close()
    
    res = []
    
    for res_owner in data_owner:
        res.append(dict(res_owner))
    return res
    
# def get_owner_one():
#     conn = sqlite3.connect(database)
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()

#     sql = "SELECT * FROM owner WHERE owner_status != 'off'"
    
#     cursor.execute(sql)
#     data_owner = cursor.fetchall()
    
#     conn.close()
    
#     res = []
    
#     for res_owner in data_owner:
#         res.append(dict(res_owner))
#     return res000000000000000


os.system('cls')

print(json.dumps(get_owner_all(), ensure_ascii=False, indent=2))


