from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from companies.models import Company


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for CustomUser model.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', CustomUser.SUPERADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with role-based access control.
    
    Roles:
    - Account Viewer: Only view tickets that the company has
    - Authorized User: Can view their company's tickets and edit the information of the company
    - Support: Can create, view tickets, and make changes to any company
    - Supervisor: Can create, view tickets, edit the companies, and edit users
    - Superadmin: Full system access (Django superuser)
    """
    
    # Role choices
    ACCOUNT_VIEWER = 'account_viewer'
    AUTHORIZED_USER = 'authorized_user'
    SUPPORT = 'support'
    SUPERVISOR = 'supervisor'
    SUPERADMIN = 'superadmin'
    
    ROLE_CHOICES = [
        (ACCOUNT_VIEWER, 'Account Viewer'),
        (AUTHORIZED_USER, 'Authorized User'),
        (SUPPORT, 'Support'),
        (SUPERVISOR, 'Supervisor'),
        (SUPERADMIN, 'Superadmin'),
    ]
    
    # User fields
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True)
    company = models.ForeignKey(
        Company, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='users'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ACCOUNT_VIEWER
    )
    
    # Django required fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['email']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        return self.first_name
    
    # Permission helper methods
    def is_account_viewer(self):
        return self.role == self.ACCOUNT_VIEWER
    
    def is_authorized_user(self):
        return self.role == self.AUTHORIZED_USER
    
    def is_support(self):
        return self.role == self.SUPPORT
    
    def is_supervisor(self):
        return self.role == self.SUPERVISOR
    
    def is_superadmin(self):
        return self.role == self.SUPERADMIN or self.is_superuser
    
    def can_view_all_tickets(self):
        """Can view tickets from all companies."""
        return self.role in [self.SUPPORT, self.SUPERVISOR, self.SUPERADMIN] or self.is_superuser
    
    def can_edit_tickets(self):
        """Can create and edit tickets."""
        return self.role in [self.SUPPORT, self.SUPERVISOR, self.SUPERADMIN] or self.is_superuser
    
    def can_edit_companies(self):
        """Can edit company information."""
        return self.role in [self.AUTHORIZED_USER, self.SUPPORT, self.SUPERVISOR, self.SUPERADMIN] or self.is_superuser
    
    def can_edit_users(self):
        """Can edit user accounts."""
        return self.role in [self.SUPERVISOR, self.SUPERADMIN] or self.is_superuser
