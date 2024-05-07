from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class AdministratorManager(BaseUserManager):
    """Manager for Administrator"""

    def create_administrator(self, email, name, password):
        if not email:
            raise ValueError("Email Not Found")
        
        email = self.normalize_email(email)
        administrator = self.model(email=email, name=name)

        administrator.set_password(password)
        administrator.is_superuser = True
        administrator.is_staff = True
        administrator.save(using=self._db)

        return administrator
    
    def create_superuser(self, email, name, password):
        return self.create_administrator(email, name, password)


class Administrator(AbstractBaseUser, PermissionsMixin):
    """DB Model for Administrators"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = AdministratorManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]


    def __str__(self):
        return f"{self.email}, {self.name}, {self.is_staff}\n"
    





