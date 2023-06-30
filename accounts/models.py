from datetime import datetime ,timedelta
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.utils import timezone 
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from backend import settings

class UserManager(BaseUserManager):
    def create_user(self,phone_number,full_name, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(phone_number=phone_number,full_name=full_name, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number=None,full_name=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        user = self.model(phone_number=phone_number,full_name=full_name, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)
    full_name = models.CharField(_("full name"), max_length=255, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=15,unique=True,blank=False)
    verification_code = models.CharField(max_length=8, blank=True, null=True)
    otp_generation_time = date_joined = models.DateTimeField(blank=True,null=True)
    address = models.CharField(_("address"), max_length=255, blank=True)
    email = models.EmailField(_("email address"))
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."),)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    objects = UserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    from datetime import timedelta

    def valid_otp(self) -> bool:
        lifespan = timedelta(minutes = 1)
        now = timezone.now()
        time_diff = now  - self.otp_generation_time

        if time_diff > lifespan:
            return False
        else:
            return True


    


   
        

      


