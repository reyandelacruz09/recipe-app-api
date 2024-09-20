from django.test import TestCase
from django.contrib.auth import get_user_model
# from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""

    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """ Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # def test_create_employee(self):
    #     user = get_user_model().objects.create_user(
    #         'test@example.com',
    #         'testpass123',
    #     )

    #     employee = models.Employee(
    #         user=user,
    #         employee_id='13413',
    #         gender=1,
    #         date_hired='2003-03-26',
    #         job_title='SE',
    #         address_1='Miami Florida',
    #         address_2='Metro Manila',
    #         phone_number='13-534-',
    #         mobile_number='09345634',
    #         martial_status=1,
    #         birthday='1995-07-09',
    #         employee_status=1,
    #         user_type=2,
    #         office_location='Makati',
    #         work_arrangement=1,
    #         contact_person_incase_of_emergency='Lordes M. Joe',
    #         cpioe_contact_no='09634534'
    #     )

        # self.assertEqual(employee.employee_id, "13413")
