from pydantic import BaseModel


class LoginInterface(BaseModel):
    username: str
    password: str


class UserInterface(BaseModel):
    first_name: str | None
    last_name: str | None
    username: str
    email: str
    password: str


class RefreshTokenInterface(BaseModel):
    refresh: str