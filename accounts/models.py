from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.mail import send_mail

class UserManager(BaseUserManager):
    def create_user(self,email,full_name, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(email=email,full_name=full_name, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None,full_name=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email,full_name, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(_("full name"), max_length=255, blank=True)
    TYPE = [
    ("CHAUFFEUR", "CHAUFFEUR"),
    ("ENTREPRISE", "ENTREPRISE"),]
    user_type = models.CharField(max_length=15,choices=TYPE,  default="CHAUFFEUR",)
    mobile = models.CharField(_("mobile"), max_length=10, blank=True)
    # photo = models.ImageField()
    email = models.EmailField(_("email address"), unique=True,blank=False)
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
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    objects = UserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class ChauffeurManager(models.Manager):
    def create_user(self , email, full_name, password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email  = email.lower()
        user = self.model(
            email = email,
            full_name = full_name
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
      
    def get_queryset(self , **extra_fields):
        queryset = super().get_queryset(**extra_fields)
        queryset = queryset.filter(user_type = "CHAUFFEUR")
        return queryset    
        
class Chauffeur(User):
    class Meta : 
        proxy = True
    objects = ChauffeurManager()
      
    def save(self , **extra_fields):
        self.user_type = "CHAUFFEUR"
        return super().save(**extra_fields)
      
class EntrepriseManager(models.Manager):
    def create_user(self , email, full_name, password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email = email.lower()
        user = self.model(
            email = email,
            full_name = full_name
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
        
    def get_queryset(self , **extra_fields):
        queryset = super().get_queryset(**extra_fields)
        queryset = queryset.filter(user_type = "ENTREPRISE")
        return queryset
      
class Entreprise(User):
    class Meta :
        proxy = True
    objects = EntrepriseManager()
      
    def save(self  , **extra_fields):
        self.user_type = "ENTREPRISE"
        return super().save(**extra_fields)

