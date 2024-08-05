from pydantic import BaseModel
from src.core.schemes.base_loggable import BaseLoggable
from typing import Final


STATUS_OK: Final = 'OK'
STATUS_ERROR: Final = 'ERROR'
NO_DETAILS = ''


class BaseResponse(BaseLoggable, BaseModel):
    status: str
    details: str
