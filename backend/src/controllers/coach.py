import psycopg
from src.models.error import ModelError
from src.types import RouterReponse
from src.models.coach import Coach
from src.models.team import Team

class CoachController:
    @staticmethod
    def index() -> RouterReponse:
        try:
            result = Coach.all()
            # Faz parse da data para usar formato ISO 8601
            for r in result:
                r["birthdate"] = r["birthdate"].isoformat()
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def show(cpf) -> RouterReponse:
        try:
            result = Coach.find_by_cpf(cpf)
            # Faz parse da data para usar formato ISO 8601
            if result:
                result["birthdate"] = result["birthdate"].isoformat()
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
            result = Coach.create(data)
            # Faz parse da data para usar formato ISO 8601
            if result:
                result["birthdate"] = result["birthdate"].isoformat()
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def update(cpf, data) -> RouterReponse:
        try:
            result = Coach.update(cpf, data)
            # Faz parse da data para usar formato ISO 8601
            if result:
                result["birthdate"] = result["birthdate"].isoformat()
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def destroy(cpf) -> RouterReponse:
        try:
            print("destroy cpf:", cpf)
            Coach.delete(cpf)
            return [200, { "status": "success", "response": None }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def get_team(cpf) -> RouterReponse:
        try:
            p = Coach.find_by_cpf(cpf)
            result = {}
            if p:
                result = Team.find_by_id(p["team_id"])
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]
