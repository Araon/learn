from fastapi import APIRouter

from schemas.user import CreateUserRequest, UserResponse
from services import permission_service as ps

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(body: CreateUserRequest):
    user = await ps.create_user(body.username)
    return UserResponse(id=user.id, username=user.username)
