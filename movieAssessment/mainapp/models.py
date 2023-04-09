from django.db import models
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# Create your models here.

class Users(AbstractBaseUser):
    first_name         = models.CharField(max_length = 100,blank=True, null=True)
    last_name          = models.CharField(max_length = 100,blank=True, null=True)
    username           = models.CharField(max_length = 100,unique=True)
    user_pic           = models.ImageField(upload_to='users/', blank=True, null=True)
    password           = models.CharField(max_length = 100)
    password_text      = models.CharField(max_length = 100)
    mobile             = models.CharField(max_length = 20, blank=True, null=True)
    email              = models.EmailField(max_length = 100,unique=True)
    created_by         = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    created_at         = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_superadmin      = models.BooleanField(default=False)
    is_admin           = models.BooleanField(default=False)
    status             = models.BooleanField(default=True)

    USERNAME_FIELD     = ('email','username')
    
    def __str__(self):
        return '%s' % (self.full_name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    class Meta:
        db_table = 'users'
        verbose_name = "User"
        verbose_name_plural = "Users" 
