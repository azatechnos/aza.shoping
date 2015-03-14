from django.db import models

# Create your models here.
from shoping.settings import FILE_UPLOAD_DIR


class CategoryImage(models.Model):
    image = models.ImageField(upload_to=FILE_UPLOAD_DIR)

class Category(models.Model):
    name = models.CharField(max_length=127)
    images = models.ManyToManyField(CategoryImage)



