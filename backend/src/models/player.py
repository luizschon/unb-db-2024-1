from psycopg import sql, OperationalError, DatabaseError
from src.database import DatabaseConnection
from src.models.error import ModelError

PLAYER_SCHEMA = ('cpf', 'name', 'birthdate', 'starting', 'photo', 'team_id')

class Player:
    @staticmethod
    def all():
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("SELECT * from player")
                rows = cur.fetchall()
            return rows
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def find_by_id(cpf):
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("SELECT * from player WHERE cpf = %s", (cpf,))
                row = cur.fetchone()
            return row
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def create(data):
        # Filtra valores recebidos que não pertencem ao schema da tabela Player
        column_value_map = {k: v for k, v in data.items() if k in PLAYER_SCHEMA}
        columns = column_value_map.keys()
        values = column_value_map.values()

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    INSERT INTO player ({columns}) VALUES ({values}) RETURNING *
                """).format(
                    columns=sql.SQL(',').join(
                        list(map(lambda c: sql.Identifier(c), columns))
                    ),
                    values=sql.SQL(',').join(
                        list(map(lambda v: sql.Literal(v), values))
                    )
                )
                cur.execute(query)
                res = cur.fetchone()
            DatabaseConnection().commit()
            return res
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            DatabaseConnection().rollback()
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))

    @staticmethod
    def update(cpf, data):
        # Filtra valores recebidos que não pertencem ao schema da tabela Player
        # e transforma em lista de tuplas
        items = [(k, v) for k, v in data.items() if k in PLAYER_SCHEMA]

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    UPDATE player SET {assigns} WHERE cpf = %s RETURNING *
                """).format(
                    assigns=sql.SQL(',').join(
                        list(map(
                            lambda i: sql.SQL("{} = {}").format(
                                sql.Identifier(i[0]), sql.Literal(i[1])
                            ),
                            items
                        ))
                    )
                )
                print(query.as_string())
                cur.execute(query, (cpf,))
                res = cur.fetchone()
            DatabaseConnection().commit()
            return res
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            DatabaseConnection().rollback()
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))

    @staticmethod
    def delete(cpf):
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("DELETE FROM player WHERE cpf = %s", (cpf,))
            DatabaseConnection().commit()
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
