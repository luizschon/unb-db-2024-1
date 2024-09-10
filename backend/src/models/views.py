from psycopg import sql, OperationalError, DatabaseError
from src.database import DatabaseConnection
from src.models.error import ModelError

class UpcomingMatches:
    @staticmethod
    def call(*args):
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("SELECT * from upcoming_matches")
                rows = cur.fetchall()
            return rows
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))

class OngoingMatches:
    @staticmethod
    def call(*args):
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("SELECT * from ongoing_matches")
                rows = cur.fetchall()
            return rows
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))

class FinishedMatches:
    @staticmethod
    def call(*args):
        try:
            with DatabaseConnection().cursor() as cur:
                cur.execute("SELECT * from finished_matches")
                rows = cur.fetchall()
            return rows
        except OperationalError:
            raise(ModelError("no database connection", "00000"))
        except DatabaseError as err:
            raise(ModelError(err.diag.message_primary, err.diag.sqlstate or "unknown"))
