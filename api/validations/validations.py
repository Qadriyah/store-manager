class ValidateInputData:

    def validate_text_fields(self, input_data):
        """
        Checks if the text field is empty

        Args:
            input_data(str): Input data coming from the text field

        Returns:
            bool: True for non-empty field, False otherwise
        """
        if not input_data.strip():
            return False
        return True

    def validate_select_fields(self, selected_option):
        """
        Checks the select input fields

        Args:
            input_data(int): option selected from the dropdown

        Returns:
            bool: True for selected, False otherwise
        """
        if selected_option == "selected":
            return False
        return True

    def validate_integer_values(self, input_data):
        """
        Checks if the input data is integer

        Args:
            input_data(int): A number coming from the form field

        Returns:
            bool: True for integer, False otherwise
        """
        try:
            int(input_data)
            return True

        except ValueError:
            return False

    def validate_password_match(self, data):
        """
        Checks if passwords match

        Args:
            data(object): Holds form data

        Returns:
            bool: True for matching, False otherwise
        """
        if data.get("password").strip() == data.get("password2").strip():
            return True
        return False

    def validate_user_data(self, data):
        """
        Validates new user input data

        Args:
            data(object): Holds form data

        Returns:
            bool:
        """
        fullname = self.validate_text_fields(data.get("fullname"))
        username = self.validate_text_fields(data.get("username"))
        password = self.validate_text_fields(data.get("password"))
        password2 = self.validate_text_fields(data.get("password2"))
        roles = self.validate_text_fields(data.get("roles"))
        if not fullname or not username or not password or not password2 or not roles:
            return False

        return True

    def validate_product_inputs(self, data):
        """
        Validates new product input data

        Args:
            data(object): Holds form data

        Returns:
            bool: True for non-empty field, False otherwise
        """
        category_id = self.validate_select_fields(data["category_id"])
        product_name = self.validate_text_fields(data.get("product_name"))
        if not category_id or not product_name:
            return False
        return True

    def validate_cart_inputs(self, data):
        """
        Validates add to cart input data

        Args:
            data(object): Holds form data

        Returns:
            bool: True for non-empty fields, False otherwise
        """
        product_id = self.validate_select_fields(data.get("product_id"))
        product_name = self.validate_text_fields(data.get("product_name"))
        quantity = self.validate_integer_values(data.get("quantity"))
        price = self.validate_integer_values(data.get("price"))
        if not product_id or not product_name or not quantity or not price:
            return False
        return True

    def validate_category_inputs(self, data):
        """
        Validates new category input data

        Args:
            data(object): Holds form data

        Returns:
            bool: True for non-empty fields, False otherwise
        """
        category_name = self.validate_text_fields(data.get("category_name"))
        price = self.validate_integer_values(data.get("price"))
        if not category_name or not price:
            return False
        return True

    def validate_inventory_inputs(self, data):
        """
        Validates new inventory item input data

        Args:
            data(object): Holds form data

        Returns:
            bool: True for non-empty fields, False otherwise
        """
        product_id = self.validate_select_fields(data.get("product_id"))
        quantity = self.validate_integer_values(data.get("quantity"))
        if not product_id or not quantity:
            return False
        return True

    def validate_register_user_inputs(self, data):
        """
        Validates new user input data

        Args:  
            data(object): Hols form data

        Returns:
            bool: True for non-empty fields, False otherwise
        """
        fullname = self.validate_text_fields(data.get("fullname"))
        username = self.validate_text_fields(data.get("username"))
        password = self.validate_text_fields(data.get("password"))
        password2 = self.validate_text_fields(data.get("password2"))
        roles = self.validate_text_fields(data.get("roles"))
        if not fullname or not username or\
         not password or not password2 or not roles:
            return False
        return True
