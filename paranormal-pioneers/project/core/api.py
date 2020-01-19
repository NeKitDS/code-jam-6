from ._core import FsApi, StdioApi, Terminal, UserApi
from ._core.vm import Env  # this will be redone in the future


class Api(FsApi, UserApi, StdioApi):
    __a = Terminal


class SimpleBoot:
    def start(self) -> Api:
        return Api(Env())
