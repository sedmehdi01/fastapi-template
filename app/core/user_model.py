from pydantic import BaseModel, Field

from auth.schemas import RoleEnum


class UserBase(BaseModel):
    user_id: str
    username: str
    role: RoleEnum
    # first_name: str
    # last_name: str
    # email: EmailStr = Field(
    #     nullable=True, index=True, sa_column_kwargs={"unique": True}
    # )
    # is_active: bool = Field(default=True)
    # is_superuser: bool = Field(default=False)
    # birthdate: datetime | None = Field(
    #     sa_column=Column(DateTime(timezone=True), nullable=True)
    # )  # birthday with timezone
    # role_id: UUID | None = Field(default=None, foreign_key="Role.id")
    # phone: str | None
    # gender: IGenderEnum | None = Field(
    #     default=IGenderEnum.other,
    #     sa_column=Column(ChoiceType(IGenderEnum, impl=String())),
    # )
    # state: str | None
    # country: str | None
    # address: str | None


class UserCreate(BaseModel):
    username: str
    hashed_password: str | None = Field(nullable=False, index=True)
    role: RoleEnum
