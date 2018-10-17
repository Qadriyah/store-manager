from datetime import datetime


class Stock:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.product_id = kwargs['product_id']
        self.product_name = kwargs['product_name']
        self.qty = kwargs['quantity']
        self.min_qty = kwargs['min_quatity']
        self.created_at = str(datetime.today().strftime("%d/%m/%Y"))

    def __repr__(self):
        return "<Stock(id={}, product_id={}, product_name={}, qty={}, min_qty={}, created_at={})>".format(self.id, self.product_id, self.product_name, self.qty, self.min_qty, self.created_at)
