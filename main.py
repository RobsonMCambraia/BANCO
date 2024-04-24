import pyodbc
from faker import Faker
import configparser

def read_config(filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    return config['database']

def connect_odbc(config):
    connection_str = (
        f"DRIVER={config['driver']};SERVER={config['server']};"
        f"DATABASE={config['database']};UID={config['username']};"
        f"PWD={config['password']};TRUSTED_CONNECTION={config['trusted_connection']}"
    )
    return pyodbc.connect(connection_str)

def insert_data(connection, data):
    try:
        cursor = connection.cursor()
        cursor.executemany("INSERT INTO ESCRITORAS (NOME) VALUES (?)", data)
        connection.commit()
        cursor.close()
    except pyodbc.DatabaseError as e:
        print(e)
        connection.rollback()
    except Exception as e:
        print(e)

fake = Faker()
fake_names = [(fake.name(),) for _ in range(100)]

config = read_config()
try:
    connection = connect_odbc(config)
    insert_data(connection, fake_names)
except pyodbc.Error as e:
    print(e)
finally:
    if connection:
        connection.close()
