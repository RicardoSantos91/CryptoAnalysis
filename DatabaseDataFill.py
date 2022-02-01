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


def columns_python_types_to_sql(col_types):

    col_types = pd.DataFrame(df_coindata.dtypes)
    col_types.columns = ['column_type']
    col_types['column_type_sql'] = 'int'
    col_types['column_type_sql'][col_types['column_type'] == 'object'] = 'varchar'
    col_types['column_type_sql'][col_types['column_type'] == 'float64'] = 'float'

    return col_types

columns_types = columns_python_types_to_sql(df_coindata.dtypes)

columns_types = columns_types.reset_index(drop=False)
columns_types = columns_types.drop(['column_type'], axis=1)
columns_types['sql_table_columns'] = columns_types['index'] + ' ' + columns_types['column_type_sql']
columns_types = columns_types.drop(['index', 'column_type_sql'], axis=1)
column_types = columns_types.values

def columns_names_list_to_string(col_names):

    col_names = ', '.join(str(element) for element in col_names)
    col_names = col_names.replace('.', '_')
    col_names = col_names.replace('[', '')
    col_names = col_names.replace(']', '')
    col_names = col_names.replace('\'', '')

    return col_names


col_names = columns_names_list_to_string(column_types)


def create_table(conn, table_name):

    sql_create_table = "CREATE TABLE " + table_name + '(' + col_names + ')'
    cursor = conn.cursor()

    try:
        cursor.execute(sql_create_table)
        conn.commit()
        print('Table ' + table_name + ' created')
    except (Exception, ps.DatabaseError) as error:
        print(error)

    return 0


connection = connect_to_database(params_dic)

create_table(connection, 'coindata')


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


## TODO: Encrypt passwords

## TODO: Create database table