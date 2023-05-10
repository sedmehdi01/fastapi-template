from pydantic import BaseModel, Field

from auth.role_schema import RoleEnum


class UserBase(BaseModel):
    username: str
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


class User(UserBase):
    hashed_password: str | None = Field(nullable=False, index=True)
    role: RoleEnum
    # groups: list["Group"] = Relationship(  # noqa: F821
    #     back_populates="users",
    #     link_model=LinkGroupUser,
    #     sa_relationship_kwargs={"lazy": "selectin"},
    # )
    # image_id: UUID | None = Field(default=None, foreign_key="ImageMedia.id")
    # image: ImageMedia = Relationship(
    #     sa_relationship_kwargs={
    #         "lazy": "joined",
    #         "primaryjoin": "User.image_id==ImageMedia.id",
    #     }
    # )
    # follower_count: int | None = Field(
    #     sa_column=Column(BigInteger(), server_default="0")
    # )
    # following_count: int | None = Field(
    #     sa_column=Column(BigInteger(), server_default="0")
    # )
