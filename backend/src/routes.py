import re
from threading import Event
from typing_extensions import Callable, Dict, List, Optional, Tuple, Union
from src.controllers.event import EventController
from src.controllers.team import TeamController
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

        # Team Actions
        ("GET", r"/team/?$"): lambda _m, _: TeamController.index(),
        ("GET", r"/team/(?P<id>\d+)/?$"): lambda m, _: TeamController.show(int(m.group('id'))),
        ("POST", r"/team/?$"): lambda _, data: TeamController.create(data),
        ("PATCH", r"/team/(?P<id>\d+)/?$"): lambda m, data: TeamController.update(int(m.group('id')), data),
        ("DELETE", r"/team/(?P<id>\d+)/?$"): lambda m, _: TeamController.destroy(int(m.group('id'))),
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
                    print(key)
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
