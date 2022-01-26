import sys
import psycopg2 as ps
from config import DB_pass
import pandas as pd
from io import StringIO
import os

# Current working directory

cwd = os.getcwd()

# Defining parameters

params_dic = {
    'host': 'localhost',
    'database': 'cryptodata',
    'user': 'postgres',
    'password': DB_pass
}


def open_csv(file, path=os.getcwd()):
    full_path = os.path.join(path, file)
    data = pd.read_csv(full_path)

    return data


df_coindata = open_csv('coindata.csv')

def connect_to_database(params):

    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = ps.connect(**params)

    except (Exception, ps.DatabaseError) as error:
        print(error)
        sys.exit()

    return conn


connection = connect_to_database(params_dic)

name_table = 'coinmetrics'
col_names = df_coindata.columns.values
col_names = [str(element) for element in col_names]
col_names = ', '.join(col_names)


sql_create_table = "create table " + name_table + '(' + col_names + ');'

cursor = connection.cursor()

cursor.execute(sql_create_table)




def copy_using_stringio_to_database(conn, df, table):

    # Save dataframe to in memory buffer

    buffer = StringIO()
    df.to_csv(buffer, index=False, index_label=None, header=False)
    buffer.seek(0)
    print('Data buffered')

    cursor = conn.cursor()
    try:
        cursor.copy_from(buffer, table, sep=',')
        conn.commit()
    except (Exception, ps.DatabaseError) as error:
        print('Error: %s' % error)
        conn.rollback()
        cursor.close()
        return 1
    print('copy_from_stringio() done')
    cursor.close()


copy_using_stringio_to_database(connection, df_coindata, 'coindata')


#TODO: Encrypt passwords