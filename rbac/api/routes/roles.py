from fastapi import APIRouter, HTTPException

from schemas.role import (
    AssignPermissionRequest,
    AssignRoleRequest,
    CreateRoleRequest,
    RoleResponse,
)
from services import permission_service as ps

router = APIRouter()


@router.post("/roles", response_model=RoleResponse, status_code=201)
async def create_role(body: CreateRoleRequest):
    role = await ps.create_role(body.name)
    return RoleResponse(id=role.id, name=role.name)


@router.post("/assign-role")
async def assign_role(body: AssignRoleRequest):
    created = await ps.assign_role(body.user_id, body.role_id)
    if not created:
        raise HTTPException(
            status_code=409,
            detail="User already has this role",
        )
    return {"success": True}


@router.post("/assign-permission")
async def assign_permission(body: AssignPermissionRequest):
    created = await ps.assign_permission(body.role_id, body.permission)
    if not created:
        raise HTTPException(
            status_code=409,
            detail="Role already has this permission",
        )
    return {"success": True}
