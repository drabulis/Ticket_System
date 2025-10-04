from django.test import TestCase
from django.utils import timezone
from .models import Ticket
from companies.models import Company
from accounts.models import CustomUser


class TicketModelTest(TestCase):
    """Tests for the Ticket model."""

    def setUp(self):
        """Set up test data."""
        self.company = Company.objects.create(
            name='Test Company',
            email='test@company.com'
        )
        self.user = CustomUser.objects.create_user(
            email='user@example.com',
            password='test123',
            first_name='Test',
            last_name='User',
            company=self.company
        )

    def test_create_ticket(self):
        """Test creating a ticket."""
        ticket = Ticket.objects.create(
            title='Test Ticket',
            description='This is a test ticket',
            company=self.company,
            created_by=self.user,
            status=Ticket.STATUS_OPEN,
            priority=Ticket.PRIORITY_HIGH
        )
        self.assertEqual(ticket.title, 'Test Ticket')
        self.assertEqual(ticket.company, self.company)
        self.assertEqual(ticket.created_by, self.user)
        self.assertEqual(ticket.status, Ticket.STATUS_OPEN)
        self.assertEqual(ticket.priority, Ticket.PRIORITY_HIGH)

    def test_ticket_str_representation(self):
        """Test the string representation of a ticket."""
        ticket = Ticket.objects.create(
            title='Support Ticket',
            description='Need help',
            company=self.company,
            created_by=self.user
        )
        expected = f"#{ticket.pk} - Support Ticket ({self.company.name})"
        self.assertEqual(str(ticket), expected)

    def test_ticket_default_values(self):
        """Test default values for status and priority."""
        ticket = Ticket.objects.create(
            title='Default Ticket',
            description='Testing defaults',
            company=self.company,
            created_by=self.user
        )
        self.assertEqual(ticket.status, Ticket.STATUS_OPEN)
        self.assertEqual(ticket.priority, Ticket.PRIORITY_MEDIUM)
        self.assertIsNone(ticket.assigned_to)
        self.assertIsNone(ticket.resolved_at)

    def test_ticket_assignment(self):
        """Test assigning a ticket to a user."""
        support_user = CustomUser.objects.create_user(
            email='support@example.com',
            password='test123',
            first_name='Support',
            last_name='User',
            role=CustomUser.SUPPORT
        )
        ticket = Ticket.objects.create(
            title='Assigned Ticket',
            description='This ticket is assigned',
            company=self.company,
            created_by=self.user,
            assigned_to=support_user
        )
        self.assertEqual(ticket.assigned_to, support_user)

    def test_ticket_ordering(self):
        """Test that tickets are ordered by creation date (newest first)."""
        ticket1 = Ticket.objects.create(
            title='First Ticket',
            description='Created first',
            company=self.company,
            created_by=self.user
        )
        ticket2 = Ticket.objects.create(
            title='Second Ticket',
            description='Created second',
            company=self.company,
            created_by=self.user
        )
        tickets = Ticket.objects.all()
        self.assertEqual(tickets[0], ticket2)
        self.assertEqual(tickets[1], ticket1)
