from .apibase import ApiBase
from .vm import Terminal


class UserApi(ApiBase):
    def terminal(self, uid: str) -> Terminal:
        return self.env.get_terminal(uid)

    def add_terminal(self, uid: str, term: Terminal) -> None:
        self.env.add_terminal(uid, term)
