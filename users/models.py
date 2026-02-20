from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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

class User(AbstractBaseUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='users', null=True, blank=True)
    supervisor = models.ForeignKey('self', on_delete=models.PROTECT, related_name='subordinate', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone', 'email']

    def has_perm(self, app_label):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return f'{self.username}, as {self.role}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    image = models.ImageField(upload_to='profile_image/', default='default.png', null=True, blank=True)
    position = models.CharField(max_length=64, null=True, blank=True)
    hired_as = models.CharField(max_length=64, null=True, blank=True)
    monthly_wage = models.IntegerField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'profile: {self.user}'
