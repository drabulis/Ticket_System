# Permission System Documentation

## Overview

The Ticket System implements a role-based access control (RBAC) system with 5 distinct user roles, each with specific permissions for viewing and managing tickets, companies, and users.

## User Roles

### 1. Account Viewer

**Purpose**: Basic users who need to track their company's tickets.

**Permissions**:
- ✓ View tickets that belong to their company
- ✗ Cannot view tickets from other companies
- ✗ Cannot create or edit tickets
- ✗ Cannot edit company information
- ✗ Cannot manage users

**Use Cases**:
- Employees tracking their department's support requests
- Stakeholders monitoring ticket progress
- Read-only access to company tickets

**Example User**: `viewer@techcorp.com`

---

### 2. Authorized User

**Purpose**: Company administrators who manage their organization's profile and tickets.

**Permissions**:
- ✓ View tickets that belong to their company
- ✓ Edit their company's information (address, phone, email, website)
- ✗ Cannot view tickets from other companies
- ✗ Cannot create or edit tickets
- ✗ Cannot manage users

**Use Cases**:
- Company administrators updating contact information
- Department heads managing company profile
- Organization representatives maintaining company data

**Example User**: `admin@techcorp.com`

---

### 3. Support

**Purpose**: Customer support staff who handle tickets across all companies.

**Permissions**:
- ✓ View all tickets from all companies
- ✓ Create new tickets
- ✓ Edit existing tickets (status, priority, assignment)
- ✓ Edit any company information
- ✗ Cannot manage user accounts

**Use Cases**:
- First-line support staff handling customer requests
- Technical support team managing ticket queue
- Customer service representatives

**Example User**: `support@system.com`

---

### 4. Supervisor

**Purpose**: Team leads and managers with full operational control.

**Permissions**:
- ✓ View all tickets from all companies
- ✓ Create and edit tickets
- ✓ Edit any company information
- ✓ Create and edit user accounts
- ✓ Assign users to companies
- ✓ Change user roles (except Superadmin)

**Use Cases**:
- Team leads managing support staff
- Department managers overseeing operations
- Administrators with full operational access

**Example User**: `supervisor@system.com`

---

### 5. Superadmin

**Purpose**: System administrators with complete access.

**Permissions**:
- ✓ All Supervisor permissions
- ✓ Full Django admin access
- ✓ Database management
- ✓ System configuration
- ✓ Can promote users to any role including Superadmin

**Use Cases**:
- System administrators
- IT staff maintaining the platform
- Initial setup and configuration

**Example User**: Created via `python manage.py createsuperuser`

---

## Permission Matrix

| Permission             | Account Viewer | Authorized User | Support | Supervisor | Superadmin |
|------------------------|----------------|-----------------|---------|------------|------------|
| View own company tickets | ✓             | ✓               | ✓       | ✓          | ✓          |
| View all tickets        | ✗             | ✗               | ✓       | ✓          | ✓          |
| Create tickets          | ✗             | ✗               | ✓       | ✓          | ✓          |
| Edit tickets            | ✗             | ✗               | ✓       | ✓          | ✓          |
| Edit own company        | ✗             | ✓               | ✓       | ✓          | ✓          |
| Edit all companies      | ✗             | ✗               | ✓       | ✓          | ✓          |
| View users              | ✗             | ✗               | ✗       | ✓          | ✓          |
| Create/edit users       | ✗             | ✗               | ✗       | ✓          | ✓          |
| System administration   | ✗             | ✗               | ✗       | ✗          | ✓          |

---

## Permission Helper Methods

The `CustomUser` model provides several helper methods to check permissions:

```python
user = CustomUser.objects.get(email='support@system.com')

# Check role
user.is_account_viewer()      # False
user.is_authorized_user()     # False
user.is_support()             # True
user.is_supervisor()          # False
user.is_superadmin()          # False

# Check permissions
user.can_view_all_tickets()   # True
user.can_edit_tickets()       # True
user.can_edit_companies()     # True
user.can_edit_users()         # False
```

---

## Implementing Permission Checks in Views

### Example: Checking if user can edit tickets

```python
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def edit_ticket(request, ticket_id):
    if not request.user.can_edit_tickets():
        return HttpResponseForbidden("You don't have permission to edit tickets.")
    
    # Handle ticket editing
    ...
```

### Example: Filtering tickets by user role

```python
from ticketing.models import Ticket

def get_user_tickets(user):
    if user.can_view_all_tickets():
        # Support, Supervisor, and Superadmin see all tickets
        return Ticket.objects.all()
    else:
        # Account Viewer and Authorized User see only their company's tickets
        if user.company:
            return Ticket.objects.filter(company=user.company)
        else:
            return Ticket.objects.none()
```

---

## Security Considerations

1. **Role Assignment**: Only Supervisors and Superadmins can change user roles
2. **Company Association**: Users should be assigned to a company (except Support/Supervisor/Superadmin)
3. **Email-based Authentication**: Users log in with their email address, not a username
4. **Password Security**: Django's built-in password hashing is used
5. **Staff Access**: Support, Supervisor, and Superadmin roles should have `is_staff=True` to access Django admin

---

## Creating Users with Different Roles

### Via Django Admin
1. Login to admin interface
2. Navigate to Users → Add User
3. Fill in email and password
4. Select role from dropdown
5. Assign company (if applicable)
6. Save

### Programmatically

```python
from accounts.models import CustomUser
from companies.models import Company

# Create a company
company = Company.objects.create(name="Tech Corp")

# Create Account Viewer
viewer = CustomUser.objects.create_user(
    email='viewer@techcorp.com',
    password='secure_password',
    first_name='John',
    last_name='Viewer',
    company=company,
    role=CustomUser.ACCOUNT_VIEWER
)

# Create Support staff
support = CustomUser.objects.create_user(
    email='support@system.com',
    password='secure_password',
    first_name='Mike',
    last_name='Support',
    role=CustomUser.SUPPORT,
    is_staff=True
)

# Create Superadmin
admin = CustomUser.objects.create_superuser(
    email='admin@system.com',
    password='secure_password',
    first_name='Admin',
    last_name='User'
)
```

---

## Upgrading/Downgrading User Roles

```python
from accounts.models import CustomUser

# Get user
user = CustomUser.objects.get(email='user@example.com')

# Upgrade to Support
user.role = CustomUser.SUPPORT
user.is_staff = True  # Grant admin access
user.save()

# Downgrade to Account Viewer
user.role = CustomUser.ACCOUNT_VIEWER
user.is_staff = False  # Remove admin access
user.save()
```

---

## Best Practices

1. **Principle of Least Privilege**: Assign users the minimum role needed for their job function
2. **Regular Audits**: Periodically review user roles and permissions
3. **Company Assignment**: Ensure Account Viewers and Authorized Users have a company assigned
4. **Staff Status**: Grant `is_staff=True` only to Support, Supervisor, and Superadmin roles
5. **Documentation**: Keep this permission documentation updated as the system evolves
6. **Testing**: Always test permission changes with each role before deploying

---

## Troubleshooting

### User can't login to admin
- Check if `is_staff=True` is set
- Verify the user role is Support, Supervisor, or Superadmin

### User can't see expected tickets
- Verify the user's company assignment
- Check the user's role permissions
- Ensure tickets are associated with the correct company

### Permission denied errors
- Confirm the user has the appropriate role
- Check if required permissions are granted
- Verify the user is active (`is_active=True`)

---

For more information, see the main [README.md](README.md) file.
