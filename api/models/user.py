from datetime import datetime


class User:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.created_at = str(datetime.today().strftime("%d/%m/%Y"))

    def __repr__(self):
        return "<User(id={}, name={}, username={})>".format(self.id, self.name, self.username)