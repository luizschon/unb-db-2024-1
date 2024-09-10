import psycopg
from src.models.error import ModelError
from src.types import RouterReponse
from src.utils import encode_base64
from src.models.player import Player
from src.models.team import Team

class PlayerController:
    @staticmethod
    def index() -> RouterReponse:
        try:
            result = Player.all()
            response = []
            for r in result:
                # Faz parse da data para usar formato ISO 8601
                r["birthdate"] = r["birthdate"].isoformat()
                team_id = r["team_id"]
                del r["team_id"]
                if team_id:
                    team = Team.find_by_id(team_id)
                    r = r | { "team": team }
                response.append(r)
            return [200, { "status": "success", "response": response }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def show(cpf: str) -> RouterReponse:
        try:
            result = Player.find_by_cpf(cpf)
            # Faz parse da data para usar formato ISO 8601
            if result:
                result["birthdate"] = result["birthdate"].isoformat()
                team_id = result["team_id"]
                del result["team_id"]
                if team_id:
                    team = Team.find_by_id(team_id)
                    result = result | { "team": team }
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
            result = Player.create(data)
            # Faz parse da data para usar formato ISO 8601
            if result:
                result["birthdate"] = result["birthdate"].isoformat()
                team_id = result["team_id"]
                del result["team_id"]
                if team_id:
                    team = Team.find_by_id(team_id)
                    result = result | { "team": team }
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
            result = Player.update(cpf, data)
            # Faz parse da data para usar formato ISO 8601
            if result:
                result["birthdate"] = result["birthdate"].isoformat()
                team_id = result["team_id"]
                del result["team_id"]
                if team_id:
                    team = Team.find_by_id(team_id)
                    result = result | { "team": team }
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
            Player.delete(cpf)
            return [200, { "status": "success", "response": None }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def get_photo(cpf) -> RouterReponse:
        try:
            result = Player.get_fields_by_cpf(cpf, "filetype", "photo")
            if result:
                result["photo"] = encode_base64(result["photo"])
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def get_team(cpf) -> RouterReponse:
        try:
            p = Player.find_by_cpf(cpf)
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
