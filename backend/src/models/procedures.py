from psycopg import sql, OperationalError, DatabaseError
from src.database import DatabaseConnection
from src.models.error import ModelError

class UpdateRankings:
    @staticmethod
    def run():
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("CALL update_winners_and_scores()")
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            DatabaseConnection().rollback()
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))
