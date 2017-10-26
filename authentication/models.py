from django.db import models

import jwt

from datetime import datetime, timedelta
import time

from django.conf import settings
from django.contrib.auth.models import ( AbstractBaseUser, BaseUserManager, PermissionsMixin )

# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise ValueError('Username is required')
        if email is None:
            raise ValueError('Email is required')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise ValueError('Superusers must have a password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({ 'id': self.pk, 'exp': int(time.mktime(dt.timetuple()))})
        return token.decode('utf-8')

    @property
    def token(self):
        return self._generate_jwt_token()
