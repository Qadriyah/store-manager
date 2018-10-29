from api.validations.is_empty import is_empty


class ValidateUserInput:

    def validate_input_data(self, request_data):
        """
        Validates input data from the new user form

        Args:
            request_data(object): request Object that holds form data

        Retruns:
            dict: {"errors", True} for no errors {"", False} if errors present
        """
        errors = {}
        if not request_data["name"].strip():
            errors.update({"name": "Fullname is required"})

        if not request_data["password2"]:
            errors.update({"password2": "Confirm password is required"})

        if request_data["password"] != request_data["password2"]:
            errors.update({"password": "Passwords do not match"})

        if not request_data["roles"]:
            errors.update({"roles": "User role is required"})

        return {
            "errors": errors,
            "is_true": is_empty(errors)
        }

    def validate_login_input(self, request_data):
        """
        Validates input data from the login form

        Args:
            request_data(object): request Object that holds form data

        Retruns:
            dict: {"errors", True} for no errors {"", False} if errors present
        """
        errors = {}
        if not request_data["username"]:
            errors.update({"username": "Username is required"})

        if not request_data["password"]:
            errors.update({"password": "Password is required"})

        return {
            "errors": errors,
            "is_true": is_empty(errors)
        }
