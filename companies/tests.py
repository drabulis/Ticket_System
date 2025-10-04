from django.test import TestCase
from .models import Company


class CompanyModelTest(TestCase):
    """Tests for the Company model."""

    def test_create_company(self):
        """Test creating a company."""
        company = Company.objects.create(
            name='Test Corp',
            address='123 Test St',
            phone='+1-555-0100',
            email='info@testcorp.com',
            website='https://testcorp.com'
        )
        self.assertEqual(company.name, 'Test Corp')
        self.assertEqual(company.email, 'info@testcorp.com')
        self.assertTrue(company.is_active)

    def test_company_str_representation(self):
        """Test the string representation of a company."""
        company = Company.objects.create(name='Test Company')
        self.assertEqual(str(company), 'Test Company')

    def test_company_unique_name(self):
        """Test that company names must be unique."""
        Company.objects.create(name='Unique Company')
        with self.assertRaises(Exception):
            Company.objects.create(name='Unique Company')

    def test_company_default_values(self):
        """Test default values for optional fields."""
        company = Company.objects.create(name='Minimal Company')
        self.assertEqual(company.address, '')
        self.assertEqual(company.phone, '')
        self.assertEqual(company.email, '')
        self.assertEqual(company.website, '')
        self.assertTrue(company.is_active)
