from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom manager for handling user creation and other user-specific methods.
class UserManager(BaseUserManager):

    # Method for creating regular users.
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Method for creating a user with realtor privileges.
    def create_realtor(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_realtor = True
        user.save(using=self._db)
        return user

    # Method for creating a superuser (admin).
    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# My Custom user model.

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_realtor = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
