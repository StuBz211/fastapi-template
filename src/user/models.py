import enum
from sqlmodel import SQLModel, Field, Relationship, Enum


class RolesEnum(enum.Enum):
    USER = 'user'
    ADMIN = 'admin'


# class Role(SQLModel, table=True):
#     pk: int | None = Field(default=None, primary_key=True)
#     name: str =  Field(index=True)
#     #users: list["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    pk: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    hashed_password: str
    activated: bool = Field(default=False)
    role: str = Field(default=RolesEnum.USER.value)
    # role_pk: int | None = Field(default=None, foreign_key="role.pk")
    # role: Role | None = Relationship(back_populates="users")


