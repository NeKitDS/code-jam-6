from project.core._core.apibase import ApiBase


class StdioApi(ApiBase):
    def send_to_all(self, msg: str) -> None:
        for usr in self.env.get_users():
            self.env.get_terminal(usr).stdout().write(msg)
