from pydantic import BaseModel


class CheckPermissionRequest(BaseModel):
    user_id: str
    permission: str
