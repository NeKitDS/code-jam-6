from .vm import Env


class ApiBase:
    def __init__(self, env: Env) -> None:
        self.env = env
