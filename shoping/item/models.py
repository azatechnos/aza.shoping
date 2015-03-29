from django.db import models

# Create your models here.
from shoping.settings import CATEGORY_UPLOAD_DIR, PRODUCT_UPLOAD_DIR


class CategoryImage(models.Model):
    image = models.ImageField(upload_to=CATEGORY_UPLOAD_DIR)
    def __unicode__(self):
        return self.image.url

class Category(models.Model):
    name = models.CharField(max_length=127)
    images = models.ManyToManyField(CategoryImage)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=127)
    image = models.ImageField(upload_to=PRODUCT_UPLOAD_DIR)
    description = models.TextField()
    price = models.IntegerField()
    ideal_for = models.CharField(max_length=127)
    stone = models.CharField(max_length=127)
    material = models.CharField(max_length=127)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name


