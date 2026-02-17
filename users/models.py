from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('email is required')
        if not username:
            raise ValueError('username is required')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(
            username=username,
            email=email,
            phone=phone,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Role(models.Model):
    name = models.CharField(max_length=64)
    priority = models.IntegerField()

    class Meta:
        ordering = ['-priority']

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='child')

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='users')
    supervisor = models.ForeignKey('self', on_delete=models.PROTECT, related_name='subordinate', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone', 'email']

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return f'{self.username}, as {self.role}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    position = models.CharField(max_length=64)
    hired_as = models.CharField(max_length=64)
    monthly_wage = models.IntegerField()
    birthday = models.DateField()
    address = models.TextField()
    bio = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'profile: {self.user}'
