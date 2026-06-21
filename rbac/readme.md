# RBAC - Role Based Access Control

A simple RBAC (Role Based Access Control) system implemented in Python. This project demonstrates core RBAC concepts: users, roles, permissions, and the relationships between them.

## Features

- User Management: Create users with unique IDs
- Role Management: Create roles with unique IDs
- Role Assignment: Assign roles to users
- Permission Management: Assign permissions to roles
- Permission Checking: Check if a user has a specific permission

## How It Works

The system uses four core data structures:

| Structure | Purpose |
|---|---|
| `users` | Stores user records (`{user_id: {id, userName}}`) |
| `roles` | Stores role records (`{role_id: {id, roleName}}`) |
| `user_roles` | Maps users to roles (`{user_id: [role_id, ...]}`) |
| `role_permission` | Maps roles to permissions (`{role_id: [permission, ...]}`) |

The permission flow: **User → Roles → Permissions**

A user's effective permissions are the union of all permissions from all roles assigned to them.

## Usage

```python
from rbac import PermissionService

service = PermissionService()

# Create users
alice = service.create_user("alice")
bob = service.create_user("bob")

# Create roles
admin = service.create_role("admin")
read = service.create_role("read")

# Assign roles
service.assign_role(alice, admin)
service.assign_role(bob, read)

# Assign permissions
service.assign_permission(admin, "create_post")
service.assign_permission(admin, "delete_post")
service.assign_permission(admin, "read_post")
service.assign_permission(read, "read_post")

# Check permissions
service.can(alice, "delete_post")   # True
service.can(bob, "delete_post")     # False
```

## Run

```bash
python main.py
```

