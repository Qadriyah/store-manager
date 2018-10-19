from datetime import datetime


class User:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.user_type = kwargs["user_type"]
        self.created_at = str(datetime.today().strftime("%d/%m/%Y"))

    def __repr__(self):
        return "<User(id={}, name={}, username={}, user_type={})>".format(self.id, self.name, self.username, self.user_type)
