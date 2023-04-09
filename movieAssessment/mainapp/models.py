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

    class Meta:
        db_table = 'users'
        verbose_name = "User"
        verbose_name_plural = "Users" 


class Movie(models.Model):
    title             = models.CharField(max_length=100)
    description 	  = models.TextField(max_length=3000)
    title_upload_date = models.DateTimeField(auto_now=True)
    movie_cover 	  = models.FileField(upload_to='movie_covers/')
    uploaded_by		  = models.ForeignKey(Users, related_name="movie_uploaded_by", on_delete=models.CASCADE, null=True, blank=True, default=None)
    updated_at 		  = models.DateTimeField(auto_now=True)
    updated_by 		  = models.ForeignKey(Users, related_name="movie_updated_by", on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'movies'
        verbose_name = "Movie"
        verbose_name_plural = "Movies" 
    

class Rating(models.Model):
    author 			= models.ForeignKey(Users, related_name="rating_author", on_delete=models.CASCADE, null=True, blank=True, default=None)
    rating_date		= models.DateTimeField(auto_now=True)
    rate_choices = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    )
    stars 			= models.IntegerField(choices=rate_choices)
    comment 		= models.TextField(max_length=4000)
    movie 			= models.ForeignKey(Movie, on_delete=models.CASCADE)
    updated_at 		= models.DateTimeField(auto_now=True)
    updated_by 		= models.ForeignKey(Users, related_name="rating_updated_by", on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.movie.title

    class Meta:
        db_table = 'ratings'
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class Report(models.Model):
    author 			= models.ForeignKey(Users, related_name="reporting_author", on_delete=models.CASCADE, null=True, blank=True, default=None)
    reporting_date  = models.DateTimeField(auto_now=True)
    comment 		= models.TextField(max_length=4000)
    report_status_choices = (
        ('Unresolved','Unresolved'),
        ('Inappropriate','Inappropriate'),
        ('Rejected','Rejected'),
    )
    stars 			= models.CharField(max_length=20, choices=report_status_choices)
    movie 			= models.ForeignKey(Movie, on_delete=models.CASCADE)
    updated_at 		= models.DateTimeField(auto_now=True)
    updated_by 		= models.ForeignKey(Users, related_name="reporting_updated_by", on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.movie.title

    class Meta:
        db_table = 'reports'
        verbose_name = "Report"
        verbose_name_plural = "reports"
