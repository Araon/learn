from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from cache.redis_client import redis
from core.database import db_session
from models.role import Role
from models.role_permission import RolePermission
from models.user import User
from models.user_role import UserRole

CACHE_TTL = 300


async def create_user(username: str) -> User:
    session = db_session.get()
    user = User(username=username)
    session.add(user)
    await session.commit()
    return user


async def create_role(rolename: str) -> Role:
    session = db_session.get()
    role = Role(name=rolename)
    session.add(role)
    await session.commit()
    return role


async def assign_role(user_id: str, role_id: str) -> bool:
    session = db_session.get()
    user_role = UserRole(user_id=user_id, role_id=role_id)
    session.add(user_role)
    try:
        await session.commit()
        await redis.delete(f"perms:{user_id}")
        return True
    except IntegrityError:
        await session.rollback()
        return False


async def assign_permission(role_id: str, permission: str) -> bool:
    session = db_session.get()
    role_permission = RolePermission(role_id=role_id, permission=permission)
    session.add(role_permission)
    try:
        await session.commit()
        # Invalidate all cached permissions (simplest approach)
        async for key in redis.scan_iter("perms:*"):
            await redis.delete(key)
        return True
    except IntegrityError:
        await session.rollback()
        return False


async def get_user_permission(user_id: str) -> set[str]:
    cache_key = f"perms:{user_id}"

    cached = await redis.smembers(cache_key)
    if cached:
        return set(cached)

    session = db_session.get()

    stmt = (
        select(RolePermission.permission)
        .join(UserRole, UserRole.role_id == RolePermission.role_id)
        .where(UserRole.user_id == user_id)
    )

    result = await session.execute(stmt)
    permissions = {row[0] for row in result.fetchall()}

    if permissions:
        await redis.sadd(cache_key, *permissions)
        await redis.expire(cache_key, CACHE_TTL)

    return permissions


async def can(user_id: str, permission: str) -> bool:
    user_permissions = await get_user_permission(user_id)
    return permission in user_permissions
