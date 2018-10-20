from datetime import datetime


class User:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.roles = kwargs["roles"]
        self.created_at = str(datetime.today().strftime("%d/%m/%Y"))

    def __repr__(self):
        return "<User(id={}, name={}, username={}, roles={})>".format(self.id, self.name, self.username, self.roles)
