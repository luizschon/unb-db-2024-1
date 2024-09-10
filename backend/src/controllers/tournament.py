import psycopg
from src.models.error import ModelError
from src.types import RouterReponse
from src.models.tournament import Tournament
from src.models.ranking import Ranking
from src.models.modality import Modality
from src.models.team import Team

class TournamentController:
    @staticmethod
    def index() -> RouterReponse:
        try:
            result = Tournament.all()
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
            result = Tournament.find_by_id(id)
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
            teams = data.get("team_ids") or []
            result = Tournament.create(data)
            # Adiciona o time no ranking
            if result and teams:
                for team_id in teams:
                    Ranking.create({
                        "tournament_id": result["id"],
                        "team_id": team_id
                    })
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
            teams = data.get("team_ids") or []
            result = Tournament.update(id, data)
            if teams:
                print("fazendo")
                teams_in_rank = [d["team_id"] for d in Ranking.where({ "tournament_id": id }) or []]
                teams_to_remove = [x for x in teams_in_rank if x not in teams]
                teams_to_add = [x for x in teams if x not in teams_in_rank]

                for team_id in teams_to_add:
                    Ranking.create({
                        "tournament_id": id,
                        "team_id": team_id
                    })

                for team_id in teams_to_remove:
                    Ranking.delete_by_ids(id, team_id)

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
            Tournament.delete(id)
            return [200, { "status": "success", "response": None }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def get_modality(id) -> RouterReponse:
        try:
            t = Tournament.find_by_id(id)
            result = {}
            if t:
                result = Modality.find_by_id(t["modality_id"])
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]

    @staticmethod
    def get_ranking(id) -> RouterReponse:
        try:
            ranking = Ranking.where({ "tournament_id": id })
            result = []
            for r in ranking or []:
                team_id = r["team_id"]
                del r["team_id"]
                team = Team.find_by_id(int(team_id))
                result.append(r | { "team": (team or {}) })
            return [200, { "status": "success", "response": result }]
        except ModelError as err:
            return [400, {
                "status": "error",
                "error_msg": err.__str__(),
                "error_code": err.error_code,
            }]
