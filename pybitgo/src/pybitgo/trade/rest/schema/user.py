from typing import TypedDict


class UserSchema(TypedDict):
    id: str
    firstName: str
    lastName: str
    email: str
