from psycopg import sql, OperationalError, DatabaseError
from src.database import DatabaseConnection
from src.models.error import ModelError

SPONSORSHIP_SCHEMA = ('event_id', 'sponsor_cnpj', 'amount')

class Sponsorship:
    @staticmethod
    def all():
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("SELECT * from sponsorship")
                rows = cur.fetchall()
            return rows
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def find_by_ids(event_id, sponsor_cnpj):
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("""
                    SELECT * from sponsorship WHERE event_id = %s sponsor_cnpj = %s
                """, (event_id, sponsor_cnpj,))
                row = cur.fetchone()
            return row
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def create(data):
        # Filtra valores recebidos que não pertencem ao schema da tabela Sponsorship
        column_value_map = {k: v for k, v in data.items() if k in SPONSORSHIP_SCHEMA}
        columns = column_value_map.keys()
        values = column_value_map.values()

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    INSERT INTO sponsorship ({columns}) VALUES ({values}) RETURNING *
                """).format(
                    columns=sql.SQL(',').join(
                        list(map(lambda c: sql.Identifier(c), columns))
                    ),
                    values=sql.SQL(',').join(
                        list(map(lambda v: sql.Literal(v), values))
                    )
                )
                cur.execute(query)
                row = cur.fetchone()
            DatabaseConnection().commit()
            return row
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            DatabaseConnection().rollback()
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))


    @staticmethod
    def update(event_id, sponsor_cnpj, data):
        # Filtra valores recebidos que não pertencem ao schema da tabela Sponsorship
        # e transforma em lista de tuplas
        items = [(k, v) for k, v in data.items() if k in SPONSORSHIP_SCHEMA]
        res = None

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    UPDATE sponsorship SET {assigns} WHERE event_id = %s AND sponsor_cnpj = %s
                    RETURNING *
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
                cur.execute(query, (event_id, sponsor_cnpj,))
                row = cur.fetchone()
            DatabaseConnection().commit()
            return row
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            DatabaseConnection().rollback()
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))

    @staticmethod
    def delete(event_id, sponsor_cnpj):
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("""
                    DELETE FROM sponsorship WHERE event_id = %s AND sponsor_cnpj = %s
                """, (event_id, sponsor_cnpj,))
            DatabaseConnection().commit()
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def where(data):
        # Filtra valores recebidos que não pertencem ao schema da tabela Sponsorship
        # e transforma em lista de tuplas
        items = [(k, v) for k, v in data.items() if k in SPONSORSHIP_SCHEMA]

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    SELECT * from sponsorship WHERE {conditions}
                """).format(
                    conditions=sql.SQL(' AND ').join(
                        list(map(
                            lambda i: sql.SQL("{} = {}").format(
                                sql.Identifier(i[0]), sql.Literal(i[1])
                            ),
                            items
                        ))
                    )
                )
                cur.execute(query)
                return cur.fetchall()
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            DatabaseConnection().rollback()
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))
