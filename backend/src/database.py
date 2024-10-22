import psycopg
from psycopg import DatabaseError
from psycopg.rows import dict_row
from threading import Lock
from dotenv import dotenv_values

config = dotenv_values(".env")

# Classe Singleton representando a conexão ao banco de dados
class DatabaseConnection:
    # Garante thread-safety instanciar o Singleton
    _lock = Lock()
    _instance = None

    def __new__(cls):
        with cls._lock:
            if cls._instance == None:
                print("Creating DatabaseConnection instance")
                cls._instance = super(DatabaseConnection, cls).__new__(cls);
            cls._instance.__init__()
        return cls._instance

    # Inicializa conexão ao banco de dados
    def __init__(self):
        try:
            if not hasattr(self, "_db_connection"):
                print("Connecting to database server...")
                self._db_connection = psycopg.connect(config.get("DATABASE_URI") or "")
                print("Connected sucessfully!")
        except DatabaseError as err:
            print("Couldn't connect to database!")
            raise

    # Re-exporta struct `Cursor` do Psycopg
    def cursor(self):
        return self._db_connection.cursor(row_factory=dict_row)

    def commit(self):
        self._db_connection.commit()

    def rollback(self):
        self._db_connection.rollback()

    # Fecha a conexão com o banco de dados
    def close(self):
        try:
            print("Disconnecting from database server...")
            self._db_connection.close()
            del self._db_connection
            print("Disconnected sucessfully!")
        except Exception as err:
            print("Couldn't disconnect from database!")
            raise(err)
