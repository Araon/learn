import uuid


class PermissionService:
    def __init__(self):

        self.users = {}
        self.roles = {}

        # permissions can only be unique
        self.permissions = set()

        self.user_roles = {}
        self.role_permission = {}

    def create_user(self, username):
        user_id = str(uuid.uuid4())

        self.users[user_id] = {"id": user_id, "userName": username}
        return user_id

    def create_role(self, rolename):
        role_id = str(uuid.uuid4())

        self.roles[role_id] = {"id": role_id, "roleName": rolename}

        return role_id

    def assign_role(self, user_id, role_id):

        if user_id not in self.user_roles:
            self.user_roles[user_id] = []
        self.user_roles[user_id].append(role_id)

    def assign_permission(self, role_id, permissions):
        if role_id not in self.role_permission:
            self.role_permission[role_id] = []
        self.role_permission[role_id].append(permissions)

    def get_user_permission(self, user_id):
        # look up user roles from self.user_roles
        # for each role check permission from self.role_permission
        # collect unique permissions into a set and return it
        user_role_ids = self.user_roles.get(user_id, [])
        permissions = set()

        for role_id in user_role_ids:
            role_perms = self.role_permission.get(role_id, [])
            permissions.update(role_perms)

        return permissions

    def can(self, user_id, permissions):
        user_perms = self.get_user_permission(user_id)
        return permissions in user_perms
