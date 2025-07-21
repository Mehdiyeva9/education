from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User, UserManager, AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class CustomUserManager(UserManager):
    def _create_user_object(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        user = self._create_user_object(email, password, **extra_fields)
        user.save(using=self._db)
        return user

    async def _acreate_user(self, email, password, **extra_fields):
        """See _create_user()"""
        user = self._create_user_object( email, password, **extra_fields)
        await user.asave(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    create_user.alters_data = True

    async def acreate_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return await self._acreate_user(email, password, **extra_fields)

    acreate_user.alters_data = True

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    create_superuser.alters_data = True

    async def acreate_superuser(
        self, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return await self._acreate_user( email, password, **extra_fields)
    
    acreate_superuser.alters_data = True

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Resource(models.Model):
    title = models.CharField(max_length=50)
    context = models.TextField()
    image = models.ImageField(upload_to="edu_photos/")
    created_by = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
class HelpForm(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mail = models.EmailField(max_length=256)
    text = models.TextField()

    def __str__(self):
        return self.text[0:50]
    
class SiteSettings(models.Model):
    banner_title = models.CharField(max_length=50, blank=True, null=True)
    banner_text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="edu_photos/", blank=True, null=True)
    subscribe_mail = models.EmailField(max_length=256, blank=True, null=True)
    terms_title = models.CharField(max_length=100, blank=True, null=True)
    terms_content = HTMLField(blank=True, null=True)
    terms_created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    privacy_title = models.CharField(max_length=100, blank=True, null=True)
    privacy_content = HTMLField(blank=True, null=True)
    privacy_created_at = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        if not self.id and SiteSettings.objects.exists():
            return None
        return super(SiteSettings,self).save(*args,**kwargs)

    def __str__ (self):
        return "Settings"
    
class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)