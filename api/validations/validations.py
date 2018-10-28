class ValidateInputData:

    def validate_empty_text_field(self, input_data):
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

    def validate_integer_values(self, input_data):
        """
        Checks if the input data is integer

        Args:
            input_data(int): A number coming from the form field

        Returns:
            bool: True for integer, False otherwise
        """
        try:
            int(input_data.strip())
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
        fullname = self.validate_empty_text_field(data.get("fullname"))
        username = self.validate_empty_text_field(data.get("username"))
        password = self.validate_empty_text_field(data.get("password"))
        password2 = self.validate_empty_text_field(data.get("password2"))
        roles = self.validate_empty_text_field(data.get("roles"))
        if not fullname or not username or not password or not password2 or not roles:
            return False

        return True
