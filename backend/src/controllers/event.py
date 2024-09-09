import psycopg
import base64
from src.utils import encode_base64
from src.models.error import ModelError
from src.types import RouterReponse
from src.models.event import Event
from src.models.sponsor import Sponsor
from src.models.sponsorship import Sponsorship

class EventController:
    @staticmethod
    def index() -> RouterReponse:
        try:
            result = Event.all()
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
            result = Event.find_by_id(id)
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
            result = Event.create(data)
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
            result = Event.update(id, data)
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
            Event.delete(id)
            return [200, { "status": "success", "response": None }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def get_sponsorships(id) -> RouterReponse:
        try:
            s = Sponsorship.where({ "event_id": int(id) })
            result = []
            for sponsorship in s or []:
                sponsor = Sponsor.find_by_cnpj(sponsorship['sponsor_cnpj'])
                if sponsor:
                    sponsor["logo"] = encode_base64(sponsor["logo"])
                    sponsor = sponsor | { "amount": sponsorship["amount"] }
                    result.append(sponsor)

            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]
