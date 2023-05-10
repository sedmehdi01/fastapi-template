from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    support = "support"
    user = "user"
