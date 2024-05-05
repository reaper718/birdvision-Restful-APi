import unittest
import json
from app import app
from flask_jwt_extended import create_access_token

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Generate an access token for testing
        with app.app_context():
            self.access_token = create_access_token(identity='admin')

    def test_get_products(self):
        response = self.app.get('/products', headers={'Authorization': f'Bearer {self.access_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_create_product(self):
        product_data = {
            "title": "Test Product",
            "description": "This is a test product",
            "price": 99.99
        }
        response = self.app.post('/products', json=product_data, headers={'Authorization': f'Bearer {self.access_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Product created successfully')

    def test_update_product(self):
        product_data = {
            "title": "Updated Product",
            "description": "This is an updated product",
            "price": 129.99
        }
        response = self.app.put('/products/9', json=product_data, headers={'Authorization': f'Bearer {self.access_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Product updated successfully')

    def test_delete_product(self):
        response = self.app.delete('/products/5', headers={'Authorization': f'Bearer {self.access_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Product deleted successfully')

if __name__ == '__main__':
    unittest.main()
