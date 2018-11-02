class Validation:

    def validate_integer(self, value):
        """
        Checks if value is a number

        Args:
            value(int): Value to be checked

        Returns:
            bool: True for integer, False otherwise
        """
        try:
            int(value)
            return True
        except ValueError:
            return False
