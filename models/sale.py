class SalesOrder:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.user_id = kwargs["user_id"]
        self.order_number = kwargs['order_number']
        self.created_at = kwargs["created_at"]

    def __repr__(self):
        return "<SalesOrder(id={}, user_id={}, order_number={}, created_at={})>".format(
            self.id,
            self.user_id,
            self.order_number,
            self.created_at
        )
