from typing import Dict
from typing_extensions import Any, List
from psycopg import sql, OperationalError, DatabaseError
from src.database import DatabaseConnection
from src.models.error import ModelError

COACH_SCHEMA = ('cpf', 'name', 'birthdate', 'photo', 'team_id')

class Coach:
    @staticmethod
    def all():
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("SELECT * from coach")
                rows = cur.fetchall()
            return rows
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def find_by_cpf(cpf) -> Dict | None:
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("SELECT * from coach WHERE cpf = %s", (cpf,))
                row = cur.fetchone()
            return row
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def create(data):
        # Filtra valores recebidos que n�o pertencem ao schema da tabela Coach
        column_value_map = {k: v for k, v in data.items() if k in COACH_SCHEMA}
        columns = column_value_map.keys()
        values = column_value_map.values()
        res = None

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    INSERT INTO coach ({columns}) VALUES ({values}) RETURNING cpf
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
            return Coach.find_by_cpf(res["cpf"])

    @staticmethod
    def update(cpf, data):
        # Filtra valores recebidos que n�o pertencem ao schema da tabela Coach
        # e transforma em lista de tuplas
        items = [(k, v) for k, v in data.items() if k in COACH_SCHEMA]
        res = None
        print(items)

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    UPDATE coach SET {assigns} WHERE cpf = %s RETURNING cpf
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
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            DatabaseConnection().rollback()
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))

        if res:
            return Coach.find_by_cpf(res["cpf"])

    @staticmethod
    def delete(cpf):
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("DELETE FROM coach WHERE cpf = %s", (cpf,))
            DatabaseConnection().commit()
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
