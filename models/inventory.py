class Inventory:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.product_id = kwargs['product_id']
        self.quantity = kwargs['quantity']
        self.stock_level = kwargs["stock_level"]
        self.min_quantity = kwargs['min_quantity']
        self.updated_at = kwargs["updated_at"]

    def __repr__(self):
        return "<Sale(id={}, product_id={}, quantity={}, stock_level={}, min_quantity={}, updated_at={})>".format(
            self.id,
            self.product_id,
            self.quantity,
            self.stock_level,
            self.min_quantity,
            self.updated_at
        )
