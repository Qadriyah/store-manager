from unittest import TestCase

from api.validations import is_empty, validate_product


class TestValidations(TestCase):

    def setUp(self):
        self.product = {
            "name": "Sugar",
            "price": 4500
        }
        self.validator = validate_product.ValidateProduct()

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
