class User:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.fullname = kwargs.get("fullname")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.roles = kwargs.get("roles")
        self.created_at = kwargs.get("created_at")
        self.modified_at = kwargs.get("modified_at")

    def __repr__(self):
        return "<User(id={}, name={}, username={}, roles={}, created_at={}, modified_at={})>".format(self.id, self.fullname, self.username, self.roles, self.created_at, self.modified_at)
