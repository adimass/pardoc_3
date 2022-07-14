import sqlite3
import os
import pandas as pd
# currentdir = os.path.dirname(os.path.abspath(__file__))

# connection = sqlite3.connect(currentdir+"pardoc.db")
# cursor = connection.cursor()

# query = """

#        select * from users

# """
# cursor.execute(query)
# connection.commit()

conn = sqlite3.connect('pardoc.db')

cursor = conn.cursor()


#for create

#for insert
# query = """
#        INSERT INTO users VALUES('id0002','aldiaz','diaz112233','admin')
# """
# cursor.execute(query)
# cursor.close()
# conn.commit()


#for read
# df = pd.read_sql_query("SELECT * from users", conn)
# print(df)

def execute_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()

