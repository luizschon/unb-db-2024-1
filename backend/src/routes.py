import re
from threading import Event
from typing_extensions import Callable, Dict, List, Optional, Tuple, Union
from src.controllers.event import EventController
from src.controllers.team import TeamController
from src.controllers.player import PlayerController
from src.controllers.coach import CoachController
from src.controllers.match import MatchController
from src.controllers.tournament import TournamentController
from src.types import RouterReponse

def not_found() -> RouterReponse:
    return [404, None]

class Router:
    path_map = {
        # Event Actions
        ("GET", r"/event/?$"): lambda _m, _: EventController.index(),
        ("GET", r"/event/(?P<id>\d+)/?$"): lambda m, _: EventController.show(int(m.group('id'))),
        ("GET", r"/event/(?P<id>\d+)/sponsorships/?$"): lambda m, _: EventController.get_sponsorships(m.group('id')),
        ("POST", r"/event/?$"): lambda _, data: EventController.create(data),
        ("PATCH", r"/event/(?P<id>\d+)/?$"): lambda m, data: EventController.update(int(m.group('id')), data),
        ("DELETE", r"/event/(?P<id>\d+)/?$"): lambda m, _: EventController.destroy(int(m.group('id'))),

        # Tournament Actions
        ("GET", r"/tournament/?$"): lambda _m, _: TournamentController.index(),
        ("GET", r"/tournament/(?P<id>\d+)/?$"): lambda m, _: TournamentController.show(int(m.group('id'))),
        ("GET", r"/tournament/(?P<id>\d+)/matches/?$"): lambda m, _: TournamentController.get_matches(int(m.group('id'))),
        ("GET", r"/tournament/(?P<id>\d+)/ranking/?$"): lambda m, _: TournamentController.get_ranking(int(m.group('id'))),
        ("GET", r"/tournament/(?P<id>\d+)/modality/?$"): lambda m, _: TournamentController.get_modality((m.group('id'))),
        ("POST", r"/tournament/?$"): lambda _, data: TournamentController.create(data),
        ("PATCH", r"/tournament/(?P<id>\d+)/?$"): lambda m, data: TournamentController.update(int(m.group('id')), data),
        ("DELETE", r"/tournament/(?P<id>\d+)/?$"): lambda m, _: TournamentController.destroy(int(m.group('id'))),

        # Team Actions
        ("GET", r"/team/?$"): lambda _m, _: TeamController.index(),
        ("GET", r"/team/(?P<id>\d+)/?$"): lambda m, _: TeamController.show(int(m.group('id'))),
        ("GET", r"/team/(?P<id>\d+)/logo$"): lambda m, _: TeamController.get_logo(int(m.group('id'))),
        ("POST", r"/team/?$"): lambda _, data: TeamController.create(data),
        ("PATCH", r"/team/(?P<id>\d+)/?$"): lambda m, data: TeamController.update(int(m.group('id')), data),
        ("DELETE", r"/team/(?P<id>\d+)/?$"): lambda m, _: TeamController.destroy(int(m.group('id'))),

        # Coach Actions
        ("GET", r"/coach/?$"): lambda _m, _: CoachController.index(),
        ("GET", r"/coach/(?P<cpf>\d+)/?$"): lambda m, _: CoachController.show(m.group('cpf')),
        ("GET", r"/coach/(?P<cpf>\d+)/team/?$"): lambda m, _: CoachController.get_team(m.group('cpf')),
        ("POST", r"/coach/?$"): lambda _, data: CoachController.create(data),
        ("PATCH", r"/coach/(?P<cpf>\d+)/?$"): lambda m, data: CoachController.update(m.group('cpf'), data),
        ("DELETE", r"/coach/(?P<cpf>\d+)/?$"): lambda m, _: CoachController.destroy(m.group('cpf')),

        # Player Actions
        ("GET", r"/player/?$"): lambda _m, _: PlayerController.index(),
        ("GET", r"/player/(?P<cpf>\d+)/?$"): lambda m, _: PlayerController.show(m.group('cpf')),
        ("GET", r"/player/(?P<cpf>\d+)/team/?$"): lambda m, _: PlayerController.get_team(m.group('cpf')),
        ("GET", r"/player/(?P<cpf>\d+)/photo/?$"): lambda m, _: PlayerController.get_photo(m.group('cpf')),
        ("POST", r"/player/?$"): lambda _, data: PlayerController.create(data),
        ("PATCH", r"/player/(?P<cpf>\d+)/?$"): lambda m, data: PlayerController.update(m.group('cpf'), data),
        ("DELETE", r"/player/(?P<cpf>\d+)/?$"): lambda m, _: PlayerController.destroy(m.group('cpf')),

        # Match Actions
        ("GET", r"/match/?$"): lambda _m, _: MatchController.index(),
        ("GET", r"/match/upcoming?$"): lambda _m, _: MatchController.get_upcoming(),
        ("GET", r"/match/ongoing?$"): lambda _m, _: MatchController.get_ongoing(),
        ("GET", r"/match/finished?$"): lambda _m, _: MatchController.get_finished(),
        ("GET", r"/match/(?P<id>\d+)/?$"): lambda m, _: MatchController.show(int(m.group('id'))),
        ("POST", r"/match/?$"): lambda _, data: MatchController.create(data),
        ("PATCH", r"/match/(?P<id>\d+)/?$"): lambda m, data: MatchController.update(int(m.group('id')), data),
        ("DELETE", r"/match/(?P<id>\d+)/?$"): lambda m, _: MatchController.destroy(int(m.group('id'))),
    }

    @classmethod
    def route(cls, method: str, path: str, data=None):
        try:
            # Filtra o PathMap pelo método HTTP usado (GET, POST, ...)
            filtered = {k: v for k, v in cls.path_map.items() if k[0] == method.upper()}
            for key, func in filtered.items():
                pattern = key[1]
                match = re.match(pattern, path)
                if match:
                    return func(match, data)
            return not_found()
        except:
            return [500, None]

    @staticmethod
    def handle_get(path, **kwargs) -> RouterReponse:
        print("GET", path)
        res = Router.route("GET", path)
        return res

    @staticmethod
    def handle_post(path, data, **kwargs) -> RouterReponse:
        print("POST", path)
        return Router.route("POST", path, data)

    @staticmethod
    def handle_patch(path, data, **kwargs) -> RouterReponse:
        print("PATCH", path)
        return Router.route("PATCH", path, data)

    @staticmethod
    def handle_delete(path, **kwargs) -> RouterReponse:
        print("DELETE", path)
        return Router.route("DELETE", path)
