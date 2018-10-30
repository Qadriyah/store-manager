class Product:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.category_id = kwargs.get("category_id")
        self.product_name = kwargs.get('product_name')
        self.created_at = kwargs.get("created_at")
        self.modified_at = kwargs.get("modified_at")

    def __repr__(self):
        return "<Product(id={}, category_id={}, product_name={}, created_at={}, modified_at={})>".format(
            self.id,
            self.category_id,
            self.product_name,
            self.created_at,
            self.modified_at
        )
