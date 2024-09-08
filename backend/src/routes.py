from typing_extensions import Dict, List, Optional, Union

RouterReponse = List[Optional[Union[int, Dict]]]

class Router:
    path_map = {}

    @staticmethod
    def handle_get(path, **kwargs) -> RouterReponse:
        print("TODO")
        return [200, None]

    @staticmethod
    def handle_post(path, data, **kwargs) -> RouterReponse:
        print("TODO")
        return [200, None]

    @staticmethod
    def handle_patch(path, data, **kwargs) -> RouterReponse:
        print("TODO")
        print(data)
        return [200, None]

    @staticmethod
    def handle_delete(path, **kwargs) -> RouterReponse:
        print("TODO")
        return [200, None]
