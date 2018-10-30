class Inventory:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.product_id = kwargs.get("product_id")
        self.quantity = kwargs.get("quantity")
        self.stock_level = kwargs.get("stock_level")
        self.min_quantity = kwargs.get("min_quantity")
        self.created_at = kwargs.get("created_at")
        self.modified_at = kwargs.get("modified_at")

    def __repr__(self):
        return "<Sale(id={}, product_id={}, quantity={}, stock_level={}, min_quantity={}, created_at={}, modified_at={})>".format(
            self.id,
            self.product_id,
            self.quantity,
            self.stock_level,
            self.min_quantity,
            self.created_at,
            self.modified_at
        )
