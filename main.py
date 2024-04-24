import pyodbc
from faker import Faker
import configparser

def read_config(filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    return config['database']

def connect_odbc(config):
    connection_str = f"DRIVER={config['driver']};SERVER={config['server']};DATABASE={config['database']};UID={config['username']};PWD={config['password']};TRUSTED_CONNECTION={config['trusted_connection']}"
    connection = pyodbc.connect(connection_str)
    cursor = connection.cursor()
    return connection, cursor

def execute_query(query, data):
    connection, cursor = connect_odbc(config)
    try:
        cursor.executemany(query, data)
        connection.commit()
    except pyodbc.DatabaseError as e:
        print(e)
        connection.rollback()
    finally:
        connection.close()

fake = Faker()
insert_names = "INSERT INTO USUARIOS (NOME) VALUES (?)"
fake_names = [(fake.name(),) for _ in range(100)]

config = read_config()
for name in fake_names:
    execute_query(insert_names, name)
