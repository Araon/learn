from pydantic import BaseModel


class CreateRoleRequest(BaseModel):
    name: str


class RoleResponse(BaseModel):
    id: str
    name: str


class AssignRoleRequest(BaseModel):
    user_id: str
    role_id: str


class AssignPermissionRequest(BaseModel):
    role_id: str
    permission: str
