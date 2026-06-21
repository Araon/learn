
from rbac import PermissionService

service = PermissionService()

alice = service.create_user("alice")
bob = service.create_user("bob")

admin = service.create_role("admin")
read = service.create_role("read")

service.assign_role(alice, admin)
service.assign_role(alice, read)

service.assign_role(bob, read)

service.assign_permission(admin, "create_post")
service.assign_permission(admin, "delete_post")
service.assign_permission(admin, "read_post")
service.assign_permission(read, "read_post")

# Test get_user_permissions
alice_perms = service.get_user_permission(alice)
print(f"Alice's permissions: {alice_perms}")

bob_perms = service.get_user_permission(bob)
print(f"Bob's permissions: {bob_perms}")

# Test can
print(f"Alice can read_post: {service.can(alice, 'read_post')}")
print(f"Alice can delete_post: {service.can(alice, 'delete_post')}")
print(f"Bob can delete_post: {service.can(bob, 'delete_post')}")


# print(json.dumps(service.users, indent=4))
# print("-"*30)
# print(json.dumps(service.roles, indent=4))
# print("-"*30)
# print(json.dumps(service.user_roles, indent=4))
