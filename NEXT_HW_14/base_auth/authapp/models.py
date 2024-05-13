from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)




class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, username, password):

        if not username:
            raise ValueError("must have username")
        if not password:
            raise ValueError("must have user password")

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):

        user = self.create_user(username=username, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    def __str__(self) -> str:
        return self.username
