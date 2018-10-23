from api.validations.is_empty import is_empty


class ValidateStockInput:

    def validate_input_data(self, request_data):
        """
        Validates input data from the new stock form

        Args:
            request_data(object): request Object that holds form data

        Retruns:
            dict: {"errors", True} for no errors {"", False} if errors present
        """
        errors = {}
        try:
            if not request_data["product_id"]:
                errors.update({"id": "Please select a product"})

            if not request_data["quantity"]:
                errors.update({"quantity": "Quantity is required"})

            int(request_data["quantity"])
        except ValueError:
            errors.update({"quantity": "Only numbers allowed for quantity"})

        return {
            "errors": errors,
            "is_true": is_empty(errors)
        }
