import psycopg
from src.models.error import ModelError
from src.types import RouterReponse
from src.utils import encode_base64
from src.models.player import Player

class PlayerController:
    @staticmethod
    def index() -> RouterReponse:
        try:
            result = Player.all()
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
    def show(cpf: str) -> RouterReponse:
        try:
            result = Player.find_by_cpf(cpf)
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
            result = Player.create(data)
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
            result = Player.update(cpf, data)
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
            result = Player.get_fields_by_cpf(cpf, "photo")
            # Faz parse da data para usar formato ISO 8601
            if result:
                result["photo"] = encode_base64(result["photo"])
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]
