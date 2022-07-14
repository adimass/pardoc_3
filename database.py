import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import sqlite3
import json

dotenv_path = Path('config/.env')
load_dotenv(dotenv_path=dotenv_path)
DATABASE = os.getenv('db_name')

conn = sqlite3.connect(DATABASE+'.db',check_same_thread=False)


#users
# userid
# name
# pass
# role
# email


def execute_query(query):

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.commit()
    except Exception as e :

        print(e)
        return 'read query error'
    
    return 'oke'

def df_query(query):

    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e :

        print(e)
        return 'read query error'
    
    
    return df

def execute_query_result(query):

    try:
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()

        cur.close()
        conn.commit()
    except Exception as e:
        print(e)
        return 'read query error'
        

    return rows


def execute_query_one(query):

    try:
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchone()[0]

        cur.close()
        conn.commit()
    except Exception as e:
        print(e)
        return 'read query error'
        

    return rows


# query="""

# insert into wallet values('%s',0)

# """%(str('haloha'))

# execute_query(query)


# email = 'adzkia@gmail.com'
# password = 'adimas112233'

# query = '''
# select *
# from users
# where email like '%s' and pass like '%s'
# '''%(str(email),str(password))

# user = df_query(query)
# print(user)

# parsed = user.to_json(orient="records")
# hasil = json.loads(parsed)

# print(hasil[0])

# for i in hasil[0].items():

#     print(i[0],i[1])
    

# df = pd.read_csv('relasi.csv')

# print(df)

# string = ""
# i = 1
# for i,row in df.iterrows():
    
#     sql = '''
#     insert into relasi values ('%s','%s')
#     '''%(row['penyakit'],row['gejala'])

#     print(sql)

#     execute_query(sql)

# query = '''

# select *
# from users

# '''
# hasil = df_query(query)
# print(hasil)


