from jwt.exceptions import InvalidTokenError


class NotValidLoginException(Exception):
    pass


class NotValidPasswordException(Exception):
    pass


class UserNotActiveException(Exception):
    pass
