class Cart:

    def __init__(self, **kwargs):
        self.product_id = kwargs['pid']
        self.name = kwargs['name']
        self.qty = kwargs["qty"]
        self.price = kwargs['price']

    def __repr__(self):
        return "<Cart(product_id={}, name={}, qty={}, price={})>".format(self.product_id, self.name, self.qty, self.price)
