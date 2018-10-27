from datetime import datetime


class User:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.roles = kwargs["roles"]
        self.created_at = kwargs["created_at"]

    def __repr__(self):
        return "<User(id={}, name={}, username={}, roles={}, created_at={})>".format(self.id, self.name, self.username, self.roles, self.created_at)
