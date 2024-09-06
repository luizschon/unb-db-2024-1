import psycopg
from dotenv import dotenv_values

config = dotenv_values(".env")

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance == None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls);
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        try:
            self._db_connection = psycopg.connect(config.get("DATABASE_URI"))
        except:
            print("Deu erro!")

    def cursor(self):
        return self._db_connection.cursor()

    def close(self):
        self._db_connection.close()

if __name__ == "__main__":
    print(config)
    db = DatabaseConnection()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM event")
        print(cur.fetchone())
    db.close()
