class SalesOrder:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.user_id = kwargs.get("user_id")
        self.order_number = kwargs.get("order_number")
        self.created_at = kwargs.get("created_at")
        self.modified_at = kwargs.get("modified_at")

    def __repr__(self):
        return "<SalesOrder(id={}, user_id={}, order_number={}, created_at={}, modified_at={})>".format(
            self.id,
            self.user_id,
            self.order_number,
            self.created_at,
            self.modified_at
        )
