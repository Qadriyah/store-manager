class Product:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.category_id = kwargs["category_id"]
        self.product_name = kwargs['product_name']
        self.created_at = kwargs["created_at"]

    def __repr__(self):
        return "<Product(id={}, category_id={}, product_name={}, created_at={})>".format(self.id, self.category_id, self.product_name, self.created_at)
