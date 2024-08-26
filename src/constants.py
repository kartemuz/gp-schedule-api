from typing import Final


class DBConstants:
    SHORT_STRING_LENGTH: Final = 100
    LONG_STRING_LENGTH: Final = 1000
    ONDELETE_CASCADE: Final = 'CASCADE'
    RELATIONSHIP_CASCADE: Final = 'all, delete-orphan'
    RELATIONSHIP_LAZY_SELECTIN: Final = 'selectin'


class ScheduleConstants:
    TAGS: Final = ['schedule']
