from loguru import logger


class BaseLoggable:
    '''Base class for logging'''

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        logger.debug(self)

    def __str__(self) -> str:
        return f'{self.__class__.__name__}={self.__dict__}'
