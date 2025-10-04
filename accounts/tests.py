from django.test import TestCase
from .models import CustomUser
from companies.models import Company


class CustomUserModelTest(TestCase):
    """Tests for the CustomUser model."""

    def setUp(self):
        """Set up test data."""
        self.company = Company.objects.create(
            name='Test Company',
            email='test@company.com'
        )

    def test_create_user(self):
        """Test creating a regular user."""
        user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            company=self.company,
            role=CustomUser.ACCOUNT_VIEWER
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.get_full_name(), 'Test User')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser."""
        superuser = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.role, CustomUser.SUPERADMIN)

    def test_account_viewer_permissions(self):
        """Test Account Viewer permissions."""
        user = CustomUser.objects.create_user(
            email='viewer@example.com',
            password='test123',
            first_name='Viewer',
            last_name='User',
            company=self.company,
            role=CustomUser.ACCOUNT_VIEWER
        )
        self.assertTrue(user.is_account_viewer())
        self.assertFalse(user.can_view_all_tickets())
        self.assertFalse(user.can_edit_tickets())
        self.assertFalse(user.can_edit_companies())
        self.assertFalse(user.can_edit_users())

    def test_authorized_user_permissions(self):
        """Test Authorized User permissions."""
        user = CustomUser.objects.create_user(
            email='authorized@example.com',
            password='test123',
            first_name='Authorized',
            last_name='User',
            company=self.company,
            role=CustomUser.AUTHORIZED_USER
        )
        self.assertTrue(user.is_authorized_user())
        self.assertFalse(user.can_view_all_tickets())
        self.assertFalse(user.can_edit_tickets())
        self.assertTrue(user.can_edit_companies())
        self.assertFalse(user.can_edit_users())

    def test_support_permissions(self):
        """Test Support permissions."""
        user = CustomUser.objects.create_user(
            email='support@example.com',
            password='test123',
            first_name='Support',
            last_name='User',
            role=CustomUser.SUPPORT
        )
        self.assertTrue(user.is_support())
        self.assertTrue(user.can_view_all_tickets())
        self.assertTrue(user.can_edit_tickets())
        self.assertTrue(user.can_edit_companies())
        self.assertFalse(user.can_edit_users())

    def test_supervisor_permissions(self):
        """Test Supervisor permissions."""
        user = CustomUser.objects.create_user(
            email='supervisor@example.com',
            password='test123',
            first_name='Supervisor',
            last_name='User',
            role=CustomUser.SUPERVISOR
        )
        self.assertTrue(user.is_supervisor())
        self.assertTrue(user.can_view_all_tickets())
        self.assertTrue(user.can_edit_tickets())
        self.assertTrue(user.can_edit_companies())
        self.assertTrue(user.can_edit_users())

    def test_user_str_representation(self):
        """Test the string representation of a user."""
        user = CustomUser.objects.create_user(
            email='test@example.com',
            password='test123',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(str(user), 'John Doe (test@example.com)')

    def test_email_normalization(self):
        """Test email normalization."""
        user = CustomUser.objects.create_user(
            email='Test@EXAMPLE.COM',
            password='test123',
            first_name='Test',
            last_name='User'
        )
        self.assertEqual(user.email, 'Test@example.com')
