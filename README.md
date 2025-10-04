# Ticket System

A Django-based ticketing system with custom user accounts and role-based access control.

## Features

### Custom User Model
The system uses a custom user model with the following fields:
- First Name
- Last Name
- Phone Number
- Email Address (used for authentication)
- Company (Foreign Key to Company model)

### User Roles

The system implements 5 user role categories with different permissions:

#### 1. Account Viewer
- **Permissions**: Only view tickets that their company has
- **Use Case**: Basic users who need to track their company's tickets

#### 2. Authorized User
- **Permissions**: 
  - View their company's tickets
  - Edit the information of their company
- **Use Case**: Company administrators who manage their organization's profile

#### 3. Support
- **Permissions**:
  - Create and view tickets for any company
  - Make changes to any company
- **Use Case**: Customer support staff who handle tickets across all companies

#### 4. Supervisor
- **Permissions**:
  - Create and view tickets for any company
  - Edit companies
  - Edit user accounts
- **Use Case**: Team leads and managers with full operational control

#### 5. Superadmin
- **Permissions**: Full system access (Django superuser)
- **Use Case**: System administrators

### Models

#### Company
- Name
- Address
- Phone
- Email
- Website
- Active status
- Creation and update timestamps

#### Ticket
- Title
- Description
- Company (Foreign Key)
- Created By (User)
- Assigned To (User)
- Status (Open, In Progress, Resolved, Closed)
- Priority (Low, Medium, High, Urgent)
- Timestamps (Created, Updated, Resolved)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/drabulis/Ticket_System.git
cd Ticket_System
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Apply migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Access the admin interface at `http://127.0.0.1:8000/admin/`

## Usage

### Creating Users

1. Log in to the Django admin interface
2. Navigate to Users section
3. Create a new user and assign:
   - Email (required for login)
   - First and Last name
   - Phone number
   - Company
   - Role (Account Viewer, Authorized User, Support, Supervisor, or Superadmin)

### Managing Companies

1. Navigate to Companies section in admin
2. Create or edit company information
3. Users can be associated with companies

### Managing Tickets

1. Navigate to Tickets section in admin
2. Create tickets with:
   - Title and description
   - Associated company
   - Status and priority
   - Assignment to users

## Permission System

The custom user model includes helper methods to check permissions:
- `can_view_all_tickets()`: Support, Supervisor, and Superadmin roles
- `can_edit_tickets()`: Support, Supervisor, and Superadmin roles
- `can_edit_companies()`: Authorized User, Support, Supervisor, and Superadmin roles
- `can_edit_users()`: Supervisor and Superadmin roles

## Project Structure

```
Ticket_System/
├── accounts/           # Custom user authentication app
├── companies/          # Company management app
├── ticketing/          # Ticket management app
├── ticket_system/      # Main project settings
├── manage.py
├── requirements.txt
└── README.md
```

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
