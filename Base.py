import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Seleccionar todos los registros ordenados por el valor actual de `index`
sql_select = '''
    SELECT  "index"
    FROM accounts_food
    ORDER BY "index" ASC
'''

cursor.execute(sql_select)
registros = cursor.fetchall()

# Reindexar los valores para que sean secuenciales
nuevo_indice = 1
for registro in registros:
    id_registro = registro[0]
    sql_update = '''
        UPDATE accounts_food
        SET "index" = ?
        WHERE "index" = ?
    '''
    cursor.execute(sql_update, (nuevo_indice, id_registro))
    nuevo_indice += 1

# Confirmar la transacción
conn.commit()

# Cerrar la conexión
conn.close()

