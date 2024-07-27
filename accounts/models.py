from django.db import models
from django.contrib.auth.models import AbstractBaseUser ,BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,email,phone_number,full_name,password):
        if not email:
            raise ValueError("email can't be empty")
        if not phone_number:
            raise ValueError("phone number can't be empty")
        if not full_name:
            raise ValueError("full name can't be empty")
        user = self.model(email=self.normalize_email(email),phone_number=phone_number,full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,phone_number,full_name,email,password):
        user = self.create_user(phone_number=phone_number,full_name=full_name,email=email,password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True)
    phone_number = models.CharField(max_length=11,unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return True


    def has_module_perms(self,app_label):
        return True


    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number
