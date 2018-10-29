from unittest import TestCase

from api.validations import validations


class TestValidations(TestCase):

    def setUp(self):
        self.validator = validations.ValidateInputData()

    def tearDown(self):
        pass

    def test_empty_text_fields(self):
        """Tests that an input field is empty"""
        self.assertFalse(self.validator.validate_text_fields(""))

    def test_non_empty_text_fields(self):
        """Tests that an input field is not empty"""
        self.assertTrue(self.validator.validate_text_fields("Sugar"))

    def test_option_not_selected(self):
        """Tests that an option is not selected from the dropdown"""
        self.assertFalse(self.validator.validate_select_fields("selected"))

    def test_option_selected(self):
        """Tests that an option is selected from the dropdown"""
        self.assertTrue(self.validator.validate_select_fields(1))

    def test_new_product_input_data(self):
        """Tests that product input fields are not empty"""
        product = dict(
            category_id=1,
            product_name="Sugar"
        )
        self.assertTrue(self.validator.validate_product_inputs(product))

    def test_missing_new_product_input_data(self):
        """Tests that product input fields are not empty"""
        product = dict(
            category_id=1,
            product_name=""
        )
        self.assertFalse(self.validator.validate_product_inputs(product))

    def test_number_entered_in_integer_fields(self):
        """Tests that the values in the number fields are integers"""
        self.assertTrue(self.validator.validate_integer_values(20))

    def test_non_number_entered_in_integer_fields(self):
        """Tests that the values in the number fields are not integers"""
        self.assertFalse(self.validator.validate_integer_values("20k"))

    def test_cart_input_data(self):
        """Tests that add to cart input fields are not empty"""
        cart_item = dict(
            product_id=1,
            product_name="Sugar",
            quantity=2,
            price=4500
        )
        self.assertTrue(self.validator.validate_cart_inputs(cart_item))

    def test_missing_cart_input_data(self):
        """Tests that add to cart input fields are empty"""
        cart_item = dict(
            product_id=1,
            product_name="",
            quantity=2,
            price=""
        )
        self.assertFalse(self.validator.validate_cart_inputs(cart_item))

    def test_category_input_data(self):
        """Tests that new category input fields are not empty"""
        category = dict(
            category_name="Gesa 500ml",
            price=1500
        )
        self.assertTrue(self.validator.validate_category_inputs(category))

    def test_missing_category_input_data(self):
        """Tests that new category input fields are empty"""
        category = dict(
            category_name="",
            price=""
        )
        self.assertFalse(self.validator.validate_category_inputs(category))

    def test_new_inventory_input_data(self):
        """Tests that the inventory input fields are not empty"""
        stock = dict(
            product_id=1,
            quantity=500
        )
        self.assertTrue(self.validator.validate_inventory_inputs(stock))

    def test_missing_new_inventory_input_data(self):
        """Tests that the form fields are empty"""
        stock = dict(
            product_id="",
            quantity=""
        )
        self.assertFalse(self.validator.validate_inventory_inputs(stock))

    def test_new_user_input_data(self):
        """Tests that new user input fields are not empty"""
        user = dict(
            fullname="Baker Sekitoleko",
            username="Baker",
            password="mukungu",
            password2="mukungu",
            roles="attendant"
        )
        self.assertTrue(self.validator.validate_user_data(user))

    def test_missing_new_user_input_data(self):
        """Tests that new user input fields are not empty"""
        user = dict(
            fullname="",
            username="Baker",
            password="",
            password2="mukungu",
            roles="attendant"
        )
        self.assertFalse(self.validator.validate_user_data(user))

    def test_passwords_match(self):
        """Tests that passwords match"""
        user = dict(
            fullname="Baker Sekitoleko",
            username="Baker",
            password="mukungu",
            password2="mukungu",
            roles="attendant"
        )
        self.assertTrue(self.validator.validate_password_match(user))

    def test_passwords_dont_match(self):
        """Tests that passwords don't match"""
        user = dict(
            fullname="Baker Sekitoleko",
            username="Baker",
            password="mukungu",
            password2="mukunguB",
            roles="attendant"
        )
        self.assertFalse(self.validator.validate_password_match(user))
