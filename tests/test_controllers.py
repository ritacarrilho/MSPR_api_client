import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from app.controllers import (
    get_customers, get_customer_by_id, create_customer, update_customer, delete_customer,
    get_all_companies, get_company_by_id, create_company, update_company, delete_company,
    get_feedbacks, get_feedback_by_id, create_feedback, update_feedback, delete_feedback,
    get_notifications, get_notification_by_id, create_notification, update_notification, delete_notification,
    get_addresses, get_address_by_id, create_address, update_address, delete_address,
    get_login_logs, get_login_log_by_id, create_login_log, update_login_log, delete_login_log,
    get_customer_companies, get_customer_company_by_ids, create_customer_company, update_customer_company, delete_customer_company
)
from app.models import Customer, Company, Feedback, Notification, Address, LoginLog, CustomerCompany
from app.schemas import (
    CustomerCreate, CustomerUpdate, CompanyCreate, CompanyUpdate,
    FeedbackCreate, FeedbackUpdate, NotificationCreate, NotificationUpdate,
    AddressCreate, AddressUpdate, LoginLogCreate, LoginLogUpdate,
    CustomerCompanyCreate, CustomerCompanyUpdate
)
from datetime import datetime

class TestController(unittest.TestCase):

    def setUp(self):
        # Set up a mock database session for each test
        self.db = MagicMock(spec=Session)

    # --------------------- Customer Tests --------------------- #

    # def test_get_customers(self):
    #     # Create mock customers
    #     mock_customers = [
    #         Customer(id_customer=1, name="John Doe"),
    #         Customer(id_customer=2, name="Jane Doe")
    #     ]

    #     self.db.query().all.return_value = mock_customers
    #     result = get_customers(self.db)
    #     self.db.query.assert_called_once_with(Customer)
    #     self.db.query().all.assert_called_once()

    #     self.assertEqual(len(result), 2)
    #     self.assertEqual(result[0].name, "John Doe")
    #     self.assertEqual(result[1].name, "Jane Doe")


    def test_get_customer_by_id(self):
        mock_customer = Customer(id_customer=1, name="John Doe")
        self.db.query().filter().first.return_value = mock_customer

        result = get_customer_by_id(self.db, 1)
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result.name, "John Doe")

    @patch("app.controllers.hash_password")
    def test_create_customer(self, mock_hash_password):
        mock_hash_password.return_value = "hashed_password"

        customer_create = CustomerCreate(
            name="John Doe",
            created_at=datetime.now(),
            username="johndoe",
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            email="johndoe@example.com",
            password_hash="password123",
            last_login=datetime.now(),
            customer_type=2,
            failed_login_attempts=0,
            preferred_contact_method=1,
            opt_in_marketing=True,
            loyalty_points=100
        )

        result = create_customer(self.db, customer_create)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        mock_hash_password.assert_called_once_with("password123")

    def test_update_customer(self):
        mock_customer = Customer(id_customer=1, name="John Doe")
        self.db.query().filter().first.return_value = mock_customer

        customer_update = CustomerUpdate(first_name="John Updated", loyalty_points=150)

        result = update_customer(self.db, 1, customer_update)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(result.first_name, "John Updated")
        self.assertEqual(result.loyalty_points, 150)

    def test_delete_customer(self):
        mock_customer = Customer(id_customer=1, name="John Doe")
        self.db.query().filter().first.return_value = mock_customer

        result = delete_customer(self.db, 1)
        self.db.delete.assert_called_once_with(mock_customer)
        self.db.commit.assert_called_once()
        self.assertEqual(result.name, "John Doe")

    # --------------------- Company Tests --------------------- #
    # def test_get_all_companies(self):
    #     mock_companies = [
    #         Company(id_company=1, company_name="Company A"),
    #         Company(id_company=2, company_name="Company B")
    #     ]

    #     self.db.query().all.return_value = mock_companies
    #     result = get_all_companies(self.db)
    #     self.db.query.assert_called_once_with(Company)
    #     self.db.query().all.assert_called_once()

    #     self.assertEqual(len(result), 2)
    #     self.assertEqual(result[0].company_name, "Company A")
    #     self.assertEqual(result[1].company_name, "Company B")

    def test_get_company_by_id(self):
        mock_company = Company(id_company=1, company_name="Company 1")
        self.db.query().filter().first.return_value = mock_company

        result = get_company_by_id(self.db, 1)
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result.company_name, "Company 1")

    def test_create_company(self):
        company_create = CompanyCreate(
            company_name="New Company",
            siret="123456789",
            address="123 Main St",
            postal_code="12345",
            city="City",
            phone="1234567890",
            email="newcompany@example.com"
        )

        result = create_company(self.db, company_create)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    # def test_update_company(self):
    #     mock_company = Company(id_company=1, company_name="Old Company")
    #     self.db.query().filter().first.return_value = mock_company

    #     company_update = CompanyUpdate(company_name="Updated Company")

    #     result = update_company(self.db, 1, company_update)
    #     self.db.commit.assert_called_once()
    #     self.db.refresh.assert_called_once()
    #     self.assertEqual(result.company_name, "Updated Company")

    def test_delete_company(self):
        mock_company = Company(id_company=1, company_name="Company 1")
        self.db.query().filter().first.return_value = mock_company

        result = delete_company(self.db, 1)
        self.db.delete.assert_called_once_with(mock_company)
        self.db.commit.assert_called_once()
        self.assertEqual(result.company_name, "Company 1")

    # --------------------- Feedback Tests --------------------- #

    # def test_get_feedbacks(self):
    #     mock_feedbacks = [
    #         Feedback(id_feedback=1, comment="Great product!"),
    #         Feedback(id_feedback=2, comment="Not bad.")
    #     ]
    #     self.db.query().offset().limit().all.return_value = mock_feedbacks

    #     result = get_feedbacks(self.db, skip=0, limit=10)
    #     self.db.query.assert_called_once_with(Feedback)
    #     self.db.query().offset.assert_called_once_with(0)
    #     self.db.query().offset().limit.assert_called_once_with(10)
    #     self.db.query().offset().limit().all.assert_called_once()

    #     self.assertEqual(len(result), 2)
    #     self.assertEqual(result[0].comment, "Great product!")
    #     self.assertEqual(result[1].comment, "Not bad.")


    def test_get_feedback_by_id(self):
        mock_feedback = Feedback(id_feedback=1, rating=5)
        self.db.query().filter().first.return_value = mock_feedback

        result = get_feedback_by_id(self.db, 1)
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result.rating, 5)

    def test_create_feedback(self):
        feedback_create = FeedbackCreate(product_id=1, rating=5, comment="Great product!", id_customer=1)

        result = create_feedback(self.db, feedback_create)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_update_feedback(self):
        mock_feedback = Feedback(id_feedback=1, rating=5)
        self.db.query().filter().first.return_value = mock_feedback

        feedback_update = FeedbackUpdate(rating=4, comment="Updated comment")

        result = update_feedback(self.db, 1, feedback_update)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(result.rating, 4)
        self.assertEqual(result.comment, "Updated comment")

    def test_delete_feedback(self):
        mock_feedback = Feedback(id_feedback=1, rating=5)
        self.db.query().filter().first.return_value = mock_feedback

        result = delete_feedback(self.db, 1)
        self.db.delete.assert_called_once_with(mock_feedback)
        self.db.commit.assert_called_once()
        self.assertEqual(result.rating, 5)

    # --------------------- Notification Tests --------------------- #

    # def test_get_notifications(self):
    #     # Create mock notifications
    #     mock_notifications = [
    #         Notification(id_notification=1, message="Message 1"),
    #         Notification(id_notification=2, message="Message 2")
    #     ]

    #     # Set up the mock to return the notifications list
    #     self.db.query().offset().limit().all.return_value = mock_notifications

    #     # Call the function
    #     result = get_notifications(self.db, skip=0, limit=10)

    #     # Assert that the query methods are called correctly
    #     self.db.query.assert_called_once_with(Notification)
    #     self.db.query().offset.assert_called_once_with(0)
    #     self.db.query().offset().limit.assert_called_once_with(10)
    #     self.db.query().offset().limit().all.assert_called_once()

    #     # Check that the result matches the mock data
    #     self.assertEqual(len(result), 2)
    #     self.assertEqual(result[0].message, "Message 1")
    #     self.assertEqual(result[1].message, "Message 2")

    def test_get_notification_by_id(self):
        mock_notification = Notification(id_notification=1, message="Test notification")
        self.db.query().filter().first.return_value = mock_notification

        result = get_notification_by_id(self.db, 1)
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result.message, "Test notification")

    def test_create_notification(self):
        notification_create = NotificationCreate(
            message="New Notification", 
            date_created=datetime.now(), 
            is_read=False, 
            type=1, 
            id_customer=1
        )

        result = create_notification(self.db, notification_create)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_update_notification(self):
        mock_notification = Notification(id_notification=1, message="Old Message")
        self.db.query().filter().first.return_value = mock_notification

        notification_update = NotificationUpdate(message="Updated Message")

        result = update_notification(self.db, 1, notification_update)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(result.message, "Updated Message")

    def test_delete_notification(self):
        mock_notification = Notification(id_notification=1, message="Message 1")
        self.db.query().filter().first.return_value = mock_notification

        result = delete_notification(self.db, 1)
        self.db.delete.assert_called_once_with(mock_notification)
        self.db.commit.assert_called_once()
        self.assertEqual(result.message, "Message 1")

    # --------------------- Address Tests --------------------- #

    # def test_get_addresses(self):
    #     mock_addresses = [Address(id_address=1, address_line1="123 Main St"), Address(id_address=2, address_line1="456 Elm St")]
    #     self.db.query().offset().limit().all.return_value = mock_addresses

    #     result = get_addresses(self.db, 0, 10)
    #     self.db.query.assert_called_once_with(Address)
    #     self.db.query().offset().limit().all.assert_called_once()

    #     self.assertEqual(len(result), 2)
    #     self.assertEqual(result[0].address_line1, "123 Main St")
    #     self.assertEqual(result[1].address_line1, "456 Elm St")

    def test_get_address_by_id(self):
        mock_address = Address(id_address=1, address_line1="123 Main St")
        self.db.query().filter().first.return_value = mock_address

        result = get_address_by_id(self.db, 1)
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result.address_line1, "123 Main St")

    def test_create_address(self):
        address_create = AddressCreate(
            address_line1="123 Main St", 
            city="City", 
            postal_code="12345", 
            country="Country", 
            address_type=1, 
            created_at=datetime.now(), 
            id_customer=1
        )

        result = create_address(self.db, address_create)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_update_address(self):
        mock_address = Address(id_address=1, address_line1="123 Main St")
        self.db.query().filter().first.return_value = mock_address

        address_update = AddressUpdate(address_line1="456 Elm St")

        result = update_address(self.db, 1, address_update)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(result.address_line1, "456 Elm St")

    def test_delete_address(self):
        mock_address = Address(id_address=1, address_line1="123 Main St")
        self.db.query().filter().first.return_value = mock_address

        result = delete_address(self.db, 1)
        self.db.delete.assert_called_once_with(mock_address)
        self.db.commit.assert_called_once()
        self.assertEqual(result.address_line1, "123 Main St")

    # --------------------- LoginLog Tests --------------------- #

    # def test_get_login_logs(self):
    #     # Create mock login logs
    #     mock_logs = [
    #         LoginLog(id_log=1, ip_address="127.0.0.1"),
    #         LoginLog(id_log=2, ip_address="192.168.0.1")
    #     ]

    #     self.db.query().offset().limit().all.return_value = mock_logs
    #     result = get_login_logs(self.db, skip=0, limit=10)

    #     self.db.query.assert_called_once_with(LoginLog)
    #     self.db.query().offset.assert_called_once_with(0)
    #     self.db.query().offset().limit.assert_called_once_with(10)
    #     self.db.query().offset().limit().all.assert_called_once()
    #     self.assertEqual(len(result), 2)
    #     self.assertEqual(result[0].ip_address, "127.0.0.1")
    #     self.assertEqual(result[1].ip_address, "192.168.0.1")


    def test_get_login_log_by_id(self):
        mock_log = LoginLog(id_log=1, ip_address="127.0.0.1")
        self.db.query().filter().first.return_value = mock_log

        result = get_login_log_by_id(self.db, 1)
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result.ip_address, "127.0.0.1")

    def test_create_login_log(self):
        login_log_create = LoginLogCreate(
            login_time=datetime.now(), 
            ip_address="127.0.0.1", 
            user_agent="Mozilla", 
            id_customer=1
        )

        result = create_login_log(self.db, login_log_create)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_update_login_log(self):
        mock_log = LoginLog(id_log=1, ip_address="127.0.0.1")
        self.db.query().filter().first.return_value = mock_log

        login_log_update = LoginLogUpdate(ip_address="192.168.0.1")

        result = update_login_log(self.db, 1, login_log_update)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(result.ip_address, "192.168.0.1")

    def test_delete_login_log(self):
        mock_log = LoginLog(id_log=1, ip_address="127.0.0.1")
        self.db.query().filter().first.return_value = mock_log

        result = delete_login_log(self.db, 1)
        self.db.delete.assert_called_once_with(mock_log)
        self.db.commit.assert_called_once()
        self.assertEqual(result.ip_address, "127.0.0.1")

    # --------------------- CustomerCompany Tests --------------------- #

    # def test_get_customer_companies(self):
    #     # Create mock customer companies
    #     mock_customer_companies = [
    #         CustomerCompany(id_customer=1, id_company=1),
    #         CustomerCompany(id_customer=2, id_company=2)
    #     ]

    #     self.db.query().offset().limit().all.return_value = mock_customer_companies

    #     result = get_customer_companies(self.db, skip=0, limit=10)
    #     self.db.query.assert_called_once_with(CustomerCompany)
    #     self.db.query().offset.assert_called_once_with(0)
    #     self.db.query().offset().limit.assert_called_once_with(10)
    #     self.db.query().offset().limit().all.assert_called_once()
    #     self.assertEqual(len(result), 2)
    #     self.assertEqual(result[0].id_customer, 1)
    #     self.assertEqual(result[1].id_company, 2)


    def test_get_customer_company_by_ids(self):
        mock_customer_company = CustomerCompany(id_customer=1, id_company=1)
        self.db.query().filter().first.return_value = mock_customer_company

        result = get_customer_company_by_ids(self.db, 1, 1)
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result.id_customer, 1)
        self.assertEqual(result.id_company, 1)

    # def test_create_customer_company(self):
    #     customer_company_create = CustomerCompanyCreate(id_customer=1, id_company=1)

    #     result = create_customer_company(self.db, customer_company_create)
    #     self.db.add.assert_called_once()
    #     self.db.commit.assert_called_once()
    #     self.db.refresh.assert_called_once()

    def test_update_customer_company(self):
        mock_customer_company = CustomerCompany(id_customer=1, id_company=1)
        self.db.query().filter().first.return_value = mock_customer_company

        customer_company_update = CustomerCompanyUpdate(id_customer=1, id_company=2)

        result = update_customer_company(self.db, 1, 1, customer_company_update)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_delete_customer_company(self):
        mock_customer_company = CustomerCompany(id_customer=1, id_company=1)
        self.db.query().filter().first.return_value = mock_customer_company

        result = delete_customer_company(self.db, 1, 1)
        self.db.delete.assert_called_once_with(mock_customer_company)
        self.db.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
