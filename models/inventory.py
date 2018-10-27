class Inventory:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.product_id = kwargs['product_id']
        self.quantity = kwargs['quantity']
        self.min_quantity = kwargs['min_quantity']
        self.created_at = kwargs["created_at"]
        self.updated_at = kwargs["updated_at"]

    def __repr__(self):
        return "<Sale(id={}, product_id={}, quantity={}, min_quantity={}, created_at={}, updated_at={})>".format(
            self.id,
            self.product_id,
            self.quantity,
            self.min_quantity,
            self.created_at,
            self.updated_at
        )
