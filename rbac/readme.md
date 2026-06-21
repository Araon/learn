# RBAC - Role Based Access Control

was messing around with RBAC concepts — users, roles, permissions, and how they connect. started as a simple python class, then kept piling stuff on it.

## what it does now

- **users** — create, each gets a uuid
- **roles** — create, each gets a uuid
- **assign roles to users** — user gets whatever permissions their roles grant
- **assign permissions to roles** — permissions follow `module:action` format (e.g. `wallet:read`, `message:write`)
- **check permissions** — does this user have this permission? yes/no

permission flow: **User → Roles → Permissions** — a user's effective permissions are whatever their roles have, unioned together.

## stack

- **FastAPI** — serves the REST api
- **PostgreSQL** — stores everything (users, roles, mappings)
- **Redis** — caches user permissions so we don't hit the db on every check (ttl of 5 mins)
- **async sqlalchemy** — db layer, sessions handled with a contextvar (no dependency injection threading `db` through every function)

## running it

```bash
# start postgres + redis
docker compose up -d

# start the api
uvicorn main:app --reload
```

## api endpoints

| method | path | what |
|---|---|---|
| `POST` | `/users` | `{"username": "alice"}` → creates user |
| `POST` | `/roles` | `{"name": "admin"}` → creates role |
| `POST` | `/assign-role` | `{"user_id": "...", "role_id": "..."}` → gives user a role |
| `POST` | `/assign-permission` | `{"role_id": "...", "permission": "wallet:read"}` → adds permission to role |
| `GET` | `/users/{id}/permissions` | returns all permissions for a user |
| `GET` | `/check` | `?user_id=X&permission=wallet:read` → true/false |

## a quick test

```bash
# create stuff
curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"username": "alice"}'
curl -X POST http://localhost:8000/roles -H "Content-Type: application/json" -d '{"name": "admin"}'

# wire them up
curl -X POST http://localhost:8000/assign-role -H "Content-Type: application/json" \
  -d '{"user_id": "<alice-id>", "role_id": "<admin-id>"}'

curl -X POST http://localhost:8000/assign-permission -H "Content-Type: application/json" \
  -d '{"role_id": "<admin-id>", "permission": "wallet:delete"}'

# check
curl "http://localhost:8000/check?user_id=<alice-id>&permission=wallet:delete"
# → {"has_permission": true}
```

## why the contextvar thing

my engineer friend at work suggested using a contextvar for the db session instead of fastapi's dependency injection. makes the service functions cleaner — no need to pass `db` as a parameter everywhere, they just grab it from the context. middleware sets it per request, services read it, everyone's happy.
