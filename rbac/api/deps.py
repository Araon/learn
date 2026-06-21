from starlette.requests import Request

from core.database import async_session, db_session


async def db_session_middleware(request: Request, call_next):
    async with async_session() as session:
        token = db_session.set(session)
        try:
            response = await call_next(request)
        finally:
            db_session.reset(token)
        return response
