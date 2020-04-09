from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager


# Create your models here.


def is_email(string):
    validator = EmailValidator()
    try:
        validator(string)
        
    except ValidationError:
        raise ValidationError("Enter proper email") 

    return True 


class Register(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(max_length=50,unique=True,validators=[is_email])
    password = models.CharField(max_length=20)
    confirmpass = models.CharField(max_length=20)

    # objects = UserManager()
    class Meta:
        managed = False
        db_table = 'register'


class Brand(models.Model):
    brand_name = models.CharField(max_length=29)
    brand_time = models.DateTimeField(blank=True)

    class Meta:
        managed = False
        db_table = 'brand'


class Category(models.Model):
    cat_name = models.CharField(max_length=29)
    cat_time = models.DateTimeField(blank=True)

    class Meta:
        managed = False
        db_table = 'category'

class Images(models.Model):
    img_id = models.AutoField(primary_key=True)
    img_path = models.TextField(blank=False, null=False)
    img_pid = models.IntegerField(blank=False, null=False)
    img_time = models.DateTimeField(blank=True, null=True,auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'images'

class Product(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=30,blank=False, null=False)
    p_caid = models.IntegerField(blank=False, null=False)
    p_brid = models.IntegerField(blank=False, null=False)
    p_mrp = models.IntegerField(blank=False, null=False)
    p_dis = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    p_descrip = models.TextField(blank=False, null=False)
    p_time = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    # p_brid = models.ForeignKey(Brand,on_delete=models.PROTECT)
    # #https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models
    # p_caid = models.ForeignKey(Category,on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'product'


