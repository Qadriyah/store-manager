class Category:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.category_name = kwargs['category_name']
        self.price = kwargs["price"]
        self.created_at = kwargs["created_at"]

    def __repr__(self):
        return "<Category(id={}, category_name={}, price={}, created_at={})>".format(self.id, self.category_name, self.price, self.created_at)
