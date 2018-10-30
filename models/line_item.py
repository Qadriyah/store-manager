class LineItem:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.product_id = kwargs.get("product_id")
        self.sales_id = kwargs.get("sales_id")
        self.product_name = kwargs.get("product_name")
        self.quantity = kwargs.get("quantity")
        self.price = kwargs.get("price")

    def __repr__(self):
        return "<LineItem(id={}, product_id={}, sales_id={}, product_name={}, quantity={}, price={})>".format(
            self.id,
            self.product_id,
            self.sales_id,
            self.product_name,
            self.quantity,
            self.price
        )
