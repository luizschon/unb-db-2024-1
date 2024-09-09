Tournamentimport psycopg
from src.models.error import ModelError
from src.types import RouterReponse
from src.models.team import Team

class TeamController:
    @staticmethod
    def index() -> RouterReponse:
        try:
            result = Team.all()
            # Faz parse da data para usar formato ISO 8601
            for r in result:
                r["date"] = r["date"].isoformat()
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def show(id) -> RouterReponse:
        try:
            result = Team.find_by_id(id)
            # Faz parse da data para usar formato ISO 8601
            if result:
                result["date"] = result["date"].isoformat()
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def create(data) -> RouterReponse:
        try:
            result = Team.create(data)
            # Faz parse da data para usar formato ISO 8601
            if result:
                result["date"] = result["date"].isoformat()
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def update(id, data) -> RouterReponse:
        try:
            result = Team.update(id, data)
            # Faz parse da data para usar formato ISO 8601
            if result:
                result["date"] = result["date"].isoformat()
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def destroy(id) -> RouterReponse:
        try:
            print("destroy id:", id)
            Team.delete(id)
            return [200, { "status": "success", "response": None }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]
