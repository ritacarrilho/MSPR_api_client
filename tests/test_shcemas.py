import unittest
from datetime import datetime
from pydantic import ValidationError
from shemcas import (
    CustomerCreate, CustomerUpdate, CompanyCreate, CompanyUpdate, 
    FeedbackCreate, FeedbackUpdate, NotificationCreate, NotificationUpdate,
    AddressCreate, AddressUpdate, LoginRequest, OrderProductSchema, CustomerOrdersResponse
)


class TestSchemas(unittest.TestCase):

    def setUp(self):
        # Set up valid data for the tests
        self.valid_customer_data = {
            "created_at": datetime.now(),
            "name": "John Doe",
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
            "email": "johndoe@example.com",
            "last_login": datetime.now(),
            "customer_type": 2,
            "failed_login_attempts": 0,
            "preferred_contact_method": 1,
            "opt_in_marketing": True,
            "loyalty_points": 100
        }

        self.valid_company_data = {
            "company_name": "Doe Industries",
            "siret": "123456789",
            "address": "123 Industrial Way",
            "postal_code": "12345",
            "city": "Industry City",
            "phone": "1234567890",
            "email": "contact@doeindustries.com"
        }

        self.valid_feedback_data = {
            "product_id": 1,
            "rating": 5,
            "comment": "Great product!",
            "created_at": datetime.now(),
            "id_customer": 1
        }

        self.valid_notification_data = {
            "message": "Your order has been shipped",
            "date_created": datetime.now(),
            "is_read": False,
            "type": 1,
            "id_customer": 1
        }

        self.valid_login_data = {
            "email": "johndoe@example.com",
            "password": "password123"
        }

        self.valid_order_product_data = {
            "productId": 1,
            "quantity": 2
        }

    # Customer tests
    def test_create_customer_valid_data(self):
        customer = CustomerCreate(**self.valid_customer_data, password_hash="hashed_password")
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.customer_type, 2)
        self.assertEqual(customer.loyalty_points, 100)

    def test_create_customer_invalid_data(self):
        invalid_data = self.valid_customer_data.copy()
        invalid_data['email'] = 'invalid-email'  
        with self.assertRaises(ValidationError):
            CustomerCreate(**invalid_data, password_hash="hashed_password")

    def test_update_customer_optional_fields(self):
        customer_update = CustomerUpdate(email="new_email@example.com", loyalty_points=200)
        self.assertEqual(customer_update.email, "new_email@example.com")
        self.assertEqual(customer_update.loyalty_points, 200)
        self.assertIsNone(customer_update.phone)

    # Company tests
    def test_create_company_valid_data(self):
        company = CompanyCreate(**self.valid_company_data)
        self.assertEqual(company.company_name, "Doe Industries")
        self.assertEqual(company.city, "Industry City")

    def test_update_company_optional_fields(self):
        company_update = CompanyUpdate(email="new_email@doeindustries.com")
        self.assertEqual(company_update.email, "new_email@doeindustries.com")
        self.assertIsNone(company_update.phone)

    # Feedback tests
    def test_create_feedback_valid_data(self):
        feedback = FeedbackCreate(**self.valid_feedback_data)
        self.assertEqual(feedback.product_id, 1)
        self.assertEqual(feedback.rating, 5)
        self.assertEqual(feedback.comment, "Great product!")

    def test_update_feedback_optional_fields(self):
        feedback_update = FeedbackUpdate(rating=4)
        self.assertEqual(feedback_update.rating, 4)
        self.assertIsNone(feedback_update.comment)

    # Notification tests
    def test_create_notification_valid_data(self):
        notification = NotificationCreate(**self.valid_notification_data)
        self.assertEqual(notification.message, "Your order has been shipped")
        self.assertFalse(notification.is_read)

    def test_update_notification_optional_fields(self):
        notification_update = NotificationUpdate(is_read=True)
        self.assertTrue(notification_update.is_read)

    # Login tests
    def test_login_request_valid_data(self):
        login_request = LoginRequest(**self.valid_login_data)
        self.assertEqual(login_request.email, "johndoe@example.com")
        self.assertEqual(login_request.password, "password123")

    # OrderProductSchema tests
    def test_order_product_schema_valid_data(self):
        order_product = OrderProductSchema(**self.valid_order_product_data)
        self.assertEqual(order_product.productId, 1)
        self.assertEqual(order_product.quantity, 2)

    # CustomerOrdersResponse test
    def test_customer_orders_response(self):
        order_data = {
            "id_order": 1,
            "createdAt": datetime.now(),
            "status": 2
        }
        response = CustomerOrdersResponse(customer_id=1, orders=[order_data])
        self.assertEqual(response.customer_id, 1)
        self.assertEqual(len(response.orders), 1)
        self.assertEqual(response.orders[0].status, 2)


if __name__ == "__main__":
    unittest.main()
