from datetime import datetime


class Sale:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.user_id = kwargs["user_id"]
        self.order_number = kwargs['order_number']
        self.product_id = kwargs['product_id']
        self.qty = kwargs['qty']
        self.price = kwargs['price']
        self.product_name = kwargs['product_name']
        self.created_at = str(datetime.today().strftime("%d/%m/%Y"))

    def __repr__(self):
        return "<Sale(id={}, product_id={}, qty={}, price={}, product_name={}, created_at={}, user_id={})>".format(
            self.id,
            self.product_id,
            self.qty,
            self.price,
            self.product_name,
            self.created_at,
            self.user_id)