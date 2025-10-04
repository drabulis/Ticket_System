from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from companies.models import Company
from ticketing.models import Ticket


class Command(BaseCommand):
    help = 'Creates sample data for testing the ticket system'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create companies
        company1, _ = Company.objects.get_or_create(
            name='Tech Corp',
            defaults={
                'address': '123 Tech Street',
                'phone': '+1-555-0101',
                'email': 'info@techcorp.com',
                'website': 'https://techcorp.com'
            }
        )
        self.stdout.write(f'Created company: {company1.name}')

        company2, _ = Company.objects.get_or_create(
            name='Business Solutions Inc',
            defaults={
                'address': '456 Business Ave',
                'phone': '+1-555-0202',
                'email': 'contact@bizsolutions.com',
                'website': 'https://bizsolutions.com'
            }
        )
        self.stdout.write(f'Created company: {company2.name}')

        # Create users with different roles
        users_data = [
            {
                'email': 'viewer@techcorp.com',
                'first_name': 'John',
                'last_name': 'Viewer',
                'phone_number': '+1-555-1001',
                'company': company1,
                'role': CustomUser.ACCOUNT_VIEWER,
                'password': 'testpass123'
            },
            {
                'email': 'admin@techcorp.com',
                'first_name': 'Jane',
                'last_name': 'Admin',
                'phone_number': '+1-555-1002',
                'company': company1,
                'role': CustomUser.AUTHORIZED_USER,
                'password': 'testpass123'
            },
            {
                'email': 'support@system.com',
                'first_name': 'Mike',
                'last_name': 'Support',
                'phone_number': '+1-555-2001',
                'company': None,
                'role': CustomUser.SUPPORT,
                'password': 'testpass123',
                'is_staff': True
            },
            {
                'email': 'supervisor@system.com',
                'first_name': 'Sarah',
                'last_name': 'Supervisor',
                'phone_number': '+1-555-3001',
                'company': None,
                'role': CustomUser.SUPERVISOR,
                'password': 'testpass123',
                'is_staff': True
            },
        ]

        created_users = []
        for user_data in users_data:
            password = user_data.pop('password')
            user, created = CustomUser.objects.get_or_create(
                email=user_data['email'],
                defaults=user_data
            )
            if created:
                user.set_password(password)
                user.save()
            created_users.append(user)
            self.stdout.write(f'Created user: {user.email} (Role: {user.get_role_display()})')

        # Create sample tickets
        tickets_data = [
            {
                'title': 'Login Issue',
                'description': 'Cannot login to the system',
                'company': company1,
                'created_by': created_users[0],
                'status': Ticket.STATUS_OPEN,
                'priority': Ticket.PRIORITY_HIGH
            },
            {
                'title': 'Feature Request',
                'description': 'Add dark mode to the interface',
                'company': company1,
                'created_by': created_users[1],
                'assigned_to': created_users[2],
                'status': Ticket.STATUS_IN_PROGRESS,
                'priority': Ticket.PRIORITY_MEDIUM
            },
            {
                'title': 'Bug Report',
                'description': 'System crashes when uploading large files',
                'company': company2,
                'created_by': created_users[2],
                'assigned_to': created_users[2],
                'status': Ticket.STATUS_OPEN,
                'priority': Ticket.PRIORITY_URGENT
            },
        ]

        for ticket_data in tickets_data:
            ticket, created = Ticket.objects.get_or_create(
                title=ticket_data['title'],
                company=ticket_data['company'],
                defaults=ticket_data
            )
            if created:
                self.stdout.write(f'Created ticket: {ticket.title} for {ticket.company.name}')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('\nYou can login with:')
        self.stdout.write('  - viewer@techcorp.com / testpass123 (Account Viewer)')
        self.stdout.write('  - admin@techcorp.com / testpass123 (Authorized User)')
        self.stdout.write('  - support@system.com / testpass123 (Support)')
        self.stdout.write('  - supervisor@system.com / testpass123 (Supervisor)')
