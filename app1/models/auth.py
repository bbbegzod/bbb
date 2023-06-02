from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models

class CustomUserManager(UserManager):
    def create_user(self, phone, password=None, is_staff=False, is_superuser=False, is_active=True, **extra_fields):
        user = self.model(phone=phone, password=password,
                          is_staff=is_staff, is_active=is_active, is_superuser=is_superuser
                          )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        return self.create_user(phone=phone, password=password, is_staff=True, is_superuser=True, is_active=True)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=13, unique=True)
    name = models.CharField(max_length=120, null=True, blank=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    object = CustomUserManager()

    USERNAME_FIELD = 'phone'

    def format(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "name": self.name,
            "is_superuser": self.is_superuser,
            "is_staff": self.is_staff,
            "is_active": self.is_active,
        }

class OTP(models.Model):
    key = models.CharField(max_length=1111)
    phone = models.CharField(max_length=14)

    is_conf = models.BooleanField(default=False)
    is_expire = models.BooleanField(default=False)
    tries = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.tries >= 3:
            self.is_expire = True

        return super(OTP, self).save(*args, **kwargs)



