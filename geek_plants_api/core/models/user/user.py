from geek_plants_api.core.models.full_name import FullName


class User:
    login: str
    password: str
    full_name: FullName

    def __init__(self, login: str, password: str, full_name: FullName):
        self.login = login
        self.password = password
        self.full_name = full_name
