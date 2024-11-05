from datetime import date

from ninja import Schema


class OkSchema(Schema):
    success: bool = True


class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # Unauthenticated users don't have the following fields, so provide defaults.
    email: str = None
    first_name: str = None
    last_name: str = None


class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class DepartmentIn(Schema):
    title: str


class DepartmentOut(Schema):
    id: int
    title: str


class Error(Schema):
    message: str
