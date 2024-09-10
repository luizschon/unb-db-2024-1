import psycopg
import base64
from src.utils import encode_base64, parse_tsrange
from src.models.error import ModelError
from src.types import RouterReponse
from src.models.match import Match
from src.models.views import FinishedMatches, OngoingMatches, UpcomingMatches

class MatchController:
    @staticmethod
    def index() -> RouterReponse:
        try:
            result = Match.all()
            response = []
            for r in result or []:
                range = r["duration"]
                del r["duration"]
                response.append(r | parse_tsrange(range))
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
            result = Match.find_by_id(id)
            if result:
                result = result | parse_tsrange(result["duration"])
                del result["duration"]
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
            result = Match.create(data)
            if result:
                result = result | parse_tsrange(result["duration"])
                del result["duration"]
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
            result = Match.update(id, data)
            if result:
                result = result | parse_tsrange(result["duration"])
                del result["duration"]
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
            Match.delete(id)
            return [200, { "status": "success", "response": None }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def get_upcoming() -> RouterReponse:
        try:
            result = UpcomingMatches.call('*')
            response = []
            for r in result or []:
                range = r["duration"]
                del r["duration"]
                response.append(r | parse_tsrange(range))
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def get_ongoing() -> RouterReponse:
        try:
            result = OngoingMatches.call('*')
            response = []
            for r in result or []:
                range = r["duration"]
                del r["duration"]
                response.append(r | parse_tsrange(range))
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def get_finished() -> RouterReponse:
        try:
            result = FinishedMatches.call('*')
            response = []
            for r in result or []:
                range = r["duration"]
                del r["duration"]
                response.append(r | parse_tsrange(range))
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]
