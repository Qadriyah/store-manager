from unittest import TestCase, skip

from api.validations import is_empty, validate_product, validate_stock


class TestValidations(TestCase):

    def setUp(self):
        self.product = {
            "name": "Sugar",
            "price": 4500
        }
        self.validator = validate_product.ValidateProduct()
        self.stock_validator = validate_stock.ValidateStockInput()

    def tearDown(self):
        pass

    def test_is_empty(self):
        """Tests if an object is empty"""
        self.assertFalse(is_empty.is_empty(self.product))

    def test_new_product_input_data(self):
        """Tests if input fields are not empty"""
        self.assertEqual(self.validator.validate_input_data(
            self.product)["is_true"], True)
        self.assertEqual(
            len(self.validator.validate_input_data(self.product)["errors"]), 0)

    def test_number_fields(self):
        """Tests that the values in the number fields are integers"""
        cart_item = dict(
            name="Milk",
            price=1500,
            qty=2
        )
        self.assertEqual(self.validator.validate_number_fields(
            cart_item)["is_true"], True)

    def test_new_stock_input_data(self):
        """Tests that the input fields are not empty"""
        new_stock = dict(
            product_id="539c3032",
            quantity=100
        )
        self.assertTrue(
            self.stock_validator.validate_input_data(new_stock)["is_true"])

    def test_non_integer_values(self):
        """Tests that the quantity and price fields contain non interger values"""
        cart_item = dict(
            name="Milk",
            price="1500P",
            qty="2Q"
        )
        self.assertEqual(self.validator.validate_number_fields(
            cart_item)["errors"]["value"], "Only numbers allowed for both price and quantity")

    def test_new_product_empty_form_fields(self):
        """Tests that the form fields are empty"""
        new_product = dict(
            name="",
            price=""
        )
        self.assertEqual(
            self.validator.validate_input_data(new_product)["is_true"],
            False
        )
        self.assertGreater(
            len(self.validator.validate_input_data(new_product)["errors"]), 0)

    def test_new_stock_empty_form_fields(self):
        """Tests that the form fields are empty"""
        new_stock = dict(
            product_id="",
            quantity=""
        )
        self.assertFalse(
            self.stock_validator.validate_input_data(new_stock)["is_true"])
        self.assertGreater(
            len(self.stock_validator.validate_input_data(new_stock)["errors"]), 0)
