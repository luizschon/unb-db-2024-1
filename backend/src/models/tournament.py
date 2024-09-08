from typing import Dict
from typing_extensions import Any, List
from psycopg import sql, OperationalError, DatabaseError
from src.database import DatabaseConnection
from src.models.error import ModelError

TOURNAMENT_SCHEMA = ('event_id', 'modality_id')

class Tournament:
    @staticmethod
    def all():
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("SELECT * from tournament")
                rows = cur.fetchall()
            return rows
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def find_by_id(id) -> Dict | None:
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("SELECT * from tournament WHERE id = %s", (id,))
                row = cur.fetchone()
            return row
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def create(data):
        # Filtra valores recebidos que não pertencem ao schema da tabela Tournament
        column_value_map = {k: v for k, v in data.items() if k in TOURNAMENT_SCHEMA}
        columns = column_value_map.keys()
        values = column_value_map.values()
        res = None

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    INSERT INTO tournament ({columns}) VALUES ({values}) RETURNING id
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
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            DatabaseConnection().rollback()
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))

        if res:
            return Tournament.find_by_id(res["id"])

    @staticmethod
    def update(id, data):
        # Filtra valores recebidos que não pertencem ao schema da tabela Tournament
        # e transforma em lista de tuplas
        items = [(k, v) for k, v in data.items() if k in TOURNAMENT_SCHEMA]
        res = None
        print(items)

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    UPDATE tournament SET {assigns} WHERE id = %s RETURNING id
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
                cur.execute(query, (id,))
                res = cur.fetchone()
            DatabaseConnection().commit()
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            DatabaseConnection().rollback()
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))

        if res:
            return Tournament.find_by_id(res["id"])

    @staticmethod
    def delete(id):
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("DELETE FROM tournament WHERE id = %s", (id,))
            DatabaseConnection().commit()
        except OperationalError:
            raise(ModelError("no database connection", "00000"))