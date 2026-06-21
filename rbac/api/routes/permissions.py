from fastapi import APIRouter, Query

from services import permission_service as ps

router = APIRouter()


@router.get("/users/{user_id}/permissions")
async def get_user_permissions(user_id: str):
    permissions = await ps.get_user_permission(user_id)
    return {"permissions": sorted(permissions)}


@router.get("/check")
async def check_permission(
    user_id: str = Query(),
    permission: str = Query(),
):
    result = await ps.can(user_id, permission)
    return {"has_permission": result}
