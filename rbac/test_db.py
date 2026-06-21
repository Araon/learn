import asyncio

from core.database import async_session, db_session, init_db, engine
from models import Role, User, UserRole
from models.role_permission import RolePermission


async def test():
    await init_db(reset=True)

    async with async_session() as session:
        token = db_session.set(session)

        # --- Create users ---
        alice = User(username="alice")
        bob = User(username="bob")
        session.add_all([alice, bob])
        await session.commit()
        await session.flush()

        # --- Create roles ---
        admin = Role(name="admin")
        reader = Role(name="read")
        session.add_all([admin, reader])
        await session.flush()

        # --- Assign roles ---
        session.add_all([
            UserRole(user_id=alice.id, role_id=admin.id),
            UserRole(user_id=alice.id, role_id=reader.id),
            UserRole(user_id=bob.id, role_id=reader.id),
        ])

        # --- Assign permissions ---
        session.add_all([
            RolePermission(role_id=admin.id, permission="create_post"),
            RolePermission(role_id=admin.id, permission="delete_post"),
            RolePermission(role_id=admin.id, permission="read_post"),
            RolePermission(role_id=reader.id, permission="read_post"),
        ])
        await session.commit()

        # --- Read back ---
        print(f"Alice: {alice.username} ({alice.id})")
        print(f"Bob: {bob.username} ({bob.id})")
        print(f"Admin: {admin.name} ({admin.id})")
        print(f"Reader: {reader.name} ({reader.id})")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test())