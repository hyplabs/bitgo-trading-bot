from enum import Enum


class StatusCodes(Enum):
    """HTTP Status Codes https://api.bitgo.com/docs/#section/HTTP-Status-Codes"""

    SUCCESS = 200
    CREATED = 201
    ACCEPTED = 202
    PARTIAL_CONTENT = 206
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    TOO_MANY_REQUESTS = 429
