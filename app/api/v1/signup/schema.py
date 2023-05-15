from pydantic import BaseModel, EmailStr


class SendEmailCodeSchema(BaseModel):
    email: EmailStr
    username: str
    password: str


class VerifyEmailSchema(BaseModel):
    email: EmailStr
    username: str
    password: str
    code: str
