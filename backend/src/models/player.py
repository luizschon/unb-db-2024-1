from typing import Dict
from typing_extensions import List
from psycopg import sql
from src.database import DatabaseConnection

EVENT_SCHEMA = ('cpf', 'name', 'birthdate', 'starting', 'photo', 'team_id')

class Event:
    @staticmethod
    def all() -> List[Dict]:
        with DatabaseConnection().cursor() as cur:
            cur.execute("SELECT * from event")
            rows = cur.fetchall()
        return rows

    @staticmethod
    def find_by_id(cpf) -> Dict | None:
        with DatabaseConnection().cursor() as cur:
            cur.execute("SELECT * from event WHERE cpf = %s", (cpf,))
            row = cur.fetchone()
        return row

    @staticmethod
    def create(**kwargs):
        # Filtra valores recebidos que não pertencem ao schema da tabela Event
        column_value_map = {k: v for k, v in kwargs.items() if k in EVENT_SCHEMA}
        columns = column_value_map.keys()
        values = column_value_map.values()

        with DatabaseConnection().cursor() as cur:
            query = sql.SQL("INSERT INTO event ({columns}) VALUES ({values})").format(
                columns=sql.SQL(',').join(list(map(lambda c: sql.Identifier(c), columns))),
                values=sql.SQL(',').join(list(map(lambda v: sql.Literal(v), values)))
            )
            cur.execute(query)
        DatabaseConnection().commit()

    @staticmethod
    def update(id, **kwargs):
        # Filtra valores recebidos que não pertencem ao schema da tabela Event
        column_value_map = {k: v for k, v in kwargs.items() if k in EVENT_SCHEMA}
        columns = column_value_map.keys()
        values = column_value_map.values()

        with DatabaseConnection().cursor() as cur:
            query = sql.SQL("UPDATE event SET ({columns}) = ({values})").format(
                columns=sql.SQL(',').join(list(map(lambda c: sql.Identifier(c), columns))),
                values=sql.SQL(',').join(list(map(lambda v: sql.Literal(v), values)))
            )
            cur.execute(query)
        DatabaseConnection().commit()

    @staticmethod
    def delete(id):
        with DatabaseConnection().cursor() as cur:
            cur.execute("DELETE FROM event WHERE cpf = %s", (cpf,))
        DatabaseConnection().commit()
