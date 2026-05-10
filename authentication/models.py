from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _
from .managers import UserManager

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    STAFF = "STAFF"
    REGULAR_USER = "USER"

    ROLES = [
        (STAFF, STAFF),
        (REGULAR_USER, REGULAR_USER)
    ]

    username = models.CharField(_("Username"), max_length=50)
    email = models.EmailField(_("Email"), max_length=254, unique=True, blank=False, null=False)
    phone = models.CharField(_("User Phone Number"), max_length=50, null=True)
    is_active = models.BooleanField(_("Active"), default=True)
    is_staff = models.BooleanField(_("Staff"), default=False)
    is_superuser = models.BooleanField(_("Superuser"), default=False)
    role = models.CharField(_("Role"), max_length=50, choices=ROLES, default=REGULAR_USER)

    credits= models.IntegerField(_("Credits"), default=0)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return self.is_superuser

    # def has_module_perms(self, app_label):
    #     return True

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-created_at"]


# class Staff(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')

#     class Meta:
#         verbose_name = _("Staff")
#         verbose_name_plural = _("Staff")

#     def __str__(self):
#         return f"Staff Profile for {self.user.email}"


# class RegularUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='regular_profile')

#     class Meta:
#         verbose_name = _("Regular User")
#         verbose_name_plural = _("Regular Users")

#     def __str__(self):
#         return f"Regular User Profile for {self.user.email}"
