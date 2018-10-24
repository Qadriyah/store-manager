from datetime import datetime


class Product:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.price = kwargs['price']
        self.quantity = 0
        self.min_quantity = 5
        self.created_at = str(datetime.today().strftime("%d/%m/%Y"))

    def __repr__(self):
        return "<Product(id={}, name={}, price={}, created_at={})>".format(self.id, self.name, self.price, self.created_at)
