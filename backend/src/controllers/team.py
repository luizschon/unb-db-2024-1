import psycopg
import base64
from src.utils import encode_base64
from src.models.error import ModelError
from src.types import RouterReponse
from src.models.team import Team

class TeamController:
    @staticmethod
    def index() -> RouterReponse:
        try:
            result = Team.all()
            for team in result or []:
                team["logo"] = encode_base64(team["logo"])
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
            if result:
                result["logo"] = encode_base64(result["logo"])
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
            print(data.keys())
            result = Team.create(data)
            if result:
                result["logo"] = encode_base64(result["logo"])
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
            if result:
                result["logo"] = encode_base64(result["logo"])
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
            Team.delete(id)
            return [200, { "status": "success", "response": None }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]
