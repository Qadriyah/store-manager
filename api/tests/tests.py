from unittest import TestCase
from datetime import datetime

class TestEndPoints(TestCase):
    def __init__(self):
        self.products = [
            {
                "product_id": 1, 
                "name": "Sugar", 
                "price": 4500,
                "created_at": datetime.utcnow
            }, 
            {
                "product_id": 2, 
                "name": "Bread", 
                "price": 2700,
                "created_at": datetime.utcnow
            }, 
            {
                "product_id": 3, 
                "name": "Milk", 
                "price": 3000,
                "created_at": datetime.utcnow
            }
        ]
    
    def test_product_list(self):
        """Test if product list is not empty"""
        self.assertGreater(len(self.products), 0)