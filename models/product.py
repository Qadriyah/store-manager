class Product:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.price = kwargs['price']
        self.created_at = kwargs["created_at"]

    def __repr__(self):
        return "<Product(id={}, name={}, price={}, created_at={})>".format(self.id, self.name, self.price, self.created_at)
