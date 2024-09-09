import psycopg
from src.models.error import ModelError
from src.types import RouterReponse
from src.models.modality import Modality

class ModalityController:
    @staticmethod
    def index() -> RouterReponse:
        try:
            result = Modality.all()
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
            result = Modality.find_by_id(id)
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
            result = Modality.create(data)
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
            result = Modality.update(id, data)
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
            Modality.delete(id)
            return [200, { "status": "success", "response": None }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]
