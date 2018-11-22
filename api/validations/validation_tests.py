from datetime import datetime


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

    def validate_date(self, date):
        """Checks if the date is valid"""
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
