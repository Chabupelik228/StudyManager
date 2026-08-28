from pydantic import BaseModel


class LoginCodeResponse(BaseModel):
    code: str


class TokenResponse(BaseModel):
    token: str


class LoginByCodeRequest(BaseModel):
    code: str
