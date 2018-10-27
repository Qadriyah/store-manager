class LineItem:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.product_id = kwargs["product_id"]
        self.sales_id = kwargs["sales_id"]
        self.product_name = kwargs['product_name']
        self.quantity = kwargs['quantity']
        self.price = kwargs['price']

    def __repr__(self):
        return "<LineItem(id={}, product_id={}, sales_id={}, product_name={}, quantity={}, price={})>".format(
            self.id,
            self.product_id,
            self.sales_id,
            self.product_name,
            self.quantity,
            self.price
        )
