import re
from threading import Event
from typing_extensions import Callable, Dict, List, Optional, Tuple, Union
from src.controllers.event import EventController
from src.types import RouterReponse

def not_found() -> RouterReponse:
    return [404, None]

class Router:
    path_map = {
        ("GET", r"/event/?$"): lambda _m, _: EventController.index(),
        ("GET", r"/event/(?P<id>\d+)/?$"): lambda m, _: EventController.show(m.group('id')),
        ("GET", r"/event/(?P<id>\d+)/sponsorships/?$"): lambda m, _: EventController.get_sponsorships(m.group('id')),
        ("POST", r"/event/?$"): lambda _, data: EventController.create(data),
        ("PATCH", r"/event/(?P<id>\d+)/?$"): lambda m, data: EventController.update(m.group('id'), data),
        ("DELETE", r"/event/(?P<id>\d+)/?$"): lambda m, _: EventController.destroy(m.group('id')),
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
        print(path)
        res = Router.route("GET", path)
        return res

    @staticmethod
    def handle_post(path, data, **kwargs) -> RouterReponse:
        print("POST", path)
        print(data)
        return Router.route("POST", path, data)

    @staticmethod
    def handle_patch(path, data, **kwargs) -> RouterReponse:
        print("PATCH", path)
        print(data)
        return Router.route("PATCH", path, data)

    @staticmethod
    def handle_delete(path, **kwargs) -> RouterReponse:
        print("DELETE", path)
        return Router.route("DELETE", path)
