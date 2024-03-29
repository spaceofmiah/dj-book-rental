from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.db import models

class CustomUserManager(BaseUserManager):
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
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name

    def is_admin(self):
        return self.is_staff
    

class Book(models.Model):
    total_pages = models.IntegerField(blank=False, null=False)
    cover_i = models.CharField(blank=False, null=False, max_length=225)
    title = models.CharField(blank=False, null=False, max_length=225)
    author = models.CharField(blank=False, null=False, max_length=225)


    def __str__(self) -> str:
        return f"{self.title} by {self.author} ({self.total_pages})"
    

class Student(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name
    

class Rental(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='rentals')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rentals')
    start_date = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateField(blank=False, null=False)

    def __str__(self) -> str:
        return f"{self.user} rented {self.book} from {self.start_date} to {self.end_date}"
    
    @property
    def is_returned(self) -> bool:
        return timezone.now().date() > self.end_date