from enum import StrEnum


class RolePermission(StrEnum):
    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"

    # def __str__(self) -> str:
    #     return self.value
