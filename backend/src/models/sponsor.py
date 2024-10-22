from psycopg import sql, OperationalError, DatabaseError
from src.database import DatabaseConnection
from src.models.error import ModelError

SPONSOR_SCHEMA = ('cnpj', 'name', 'logo', 'filetype')

class Sponsor:
    @staticmethod
    def all():
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("SELECT cnpj, name from sponsor")
                rows = cur.fetchall()
            return rows
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def find_by_cnpj(cnpj):
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("SELECT cnpj, name from sponsor WHERE cnpj = %s", (cnpj,))
                row = cur.fetchone()
            return row
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def get_fields_by_cnpj(cnpj, *args):
        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    SELECT {fields} from sponsor WHERE cnpj = %s
                """).format(
                    fields=sql.SQL(',').join(list(map(lambda a: sql.Identifier(a), args)))
                )
                cur.execute(query, (cnpj,))
                row = cur.fetchone()
            return row
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def create(data):
        # Filtra valores recebidos que não pertencem ao schema da tabela Sponsor
        column_value_map = {k: v for k, v in data.items() if k in SPONSOR_SCHEMA}
        columns = column_value_map.keys()
        values = column_value_map.values()

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    INSERT INTO sponsor ({columns}) VALUES ({values}) RETURNING cnpj, name
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
    def update(cnpj, data):
        # Filtra valores recebidos que não pertencem ao schema da tabela Sponsor
        # e transforma em lista de tuplas
        items = [(k, v) for k, v in data.items() if k in SPONSOR_SCHEMA]

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    UPDATE sponsor SET {assigns} WHERE cnpj = %s RETURNING cnpj, name
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
                cur.execute(query, (cnpj,))
                res = cur.fetchone()
            DatabaseConnection().commit()
            return res
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            DatabaseConnection().rollback()
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))

    @staticmethod
    def delete(cnpj):
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("DELETE FROM sponsor WHERE cnpj = %s", (cnpj,))
            DatabaseConnection().commit()
        except OperationalError:
            raise(ModelError("no database connection", "00000"))

    @staticmethod
    def where(data):
        # Filtra valores recebidos que não pertencem ao schema da tabela Sponsor
        # e transforma em lista de tuplas
        items = [(k, v) for k, v in data.items() if k in SPONSOR_SCHEMA]

        try:
            with DatabaseConnection().cursor() as cur:
                query = sql.SQL("""
                    SELECT cnpj, name from sponsor WHERE {conditions}
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
