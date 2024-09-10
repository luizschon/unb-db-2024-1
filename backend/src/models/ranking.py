from psycopg import sql, OperationalError, DatabaseError
from src.database import DatabaseConnection
from src.models.error import ModelError

RANKING_SCHEMA = ('tournament_id', 'team_id')

class Ranking:
    @staticmethod
    def all():
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("SELECT * from ranking")
                rows = cur.fetchall()
            return rows
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def find_by_ids(tournament_id, team_id):
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute(
                    """SELECT * from ranking WHERE tournament_id = %s AND team_id = %s
                """, (tournament_id, team_id,))
                row = cur.fetchone()
            return row
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def create(data):
        # Filtra valores recebidos que não pertencem ao schema da tabela Ranking
        column_value_map = {k: v for k, v in data.items() if k in RANKING_SCHEMA}
        columns = column_value_map.keys()
        values = column_value_map.values()

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    INSERT INTO ranking ({columns}) VALUES ({values}) RETURNING *
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
    def delete_by_ids(tournament_id, team_id):
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute(
                    """DELETE FROM ranking WHERE tournament_id = %s AND team_id = %s
                """, (tournament_id, team_id,))
            DatabaseConnection().commit()
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def where(data):
        # Filtra valores recebidos que não pertencem ao schema da tabela Ranking
        # e transforma em lista de tuplas
        items = [(k, v) for k, v in data.items() if k in RANKING_SCHEMA]

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    SELECT * from ranking WHERE {conditions}
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
                print(query.as_string())
                cur.execute(query)
                return cur.fetchall()
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            DatabaseConnection().rollback()
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))
