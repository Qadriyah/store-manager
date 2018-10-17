from api.validations.is_empty import is_empty


class ValidateProduct:

    def validate_input_data(self, request_data):
        """
        Validates input data from the new product form

        Args:
            request_data(object): request Object that holds form data

        Retruns:
            dict: {"errors", True} if there were any errors {"", False} if there were no errors
        """
        errors = {}
        if not request_data["name"].strip():
            errors.update({"name": "Product name is required"})

        if not request_data["price"]:
            errors.update({"price": "Product price is required"})

        return {
            "errors": errors,
            "is_true": is_empty(errors)
        }
