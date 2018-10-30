class Category:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.category_name = kwargs.get("category_name")
        self.price = kwargs.get("price")
        self.created_at = kwargs.get("created_at")
        self.modified_at = kwargs.get("modified_at")

    def __repr__(self):
        return "<Category(id={}, category_name={}, price={}, created_at={}, modified_at={})>".format(
            self.id, 
            self.category_name, 
            self.price, 
            self.created_at, 
            self.modified_at
        )
