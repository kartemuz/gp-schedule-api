class FullName:
    surname: str
    name: str
    patronymic: str

    def __init__(self, surname: str, name: str, patronymic: str):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
