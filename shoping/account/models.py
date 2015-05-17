__author__ = 'aamirbhatt'

from django.contrib.auth import user_logged_in
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

ACCOUNT_ADMIN = 'A'
SUPER_ADMIN = 'S'
TECH_ADMIN = 'T'
CUSTOMER = 'C'

USER_TYPES = (
    (SUPER_ADMIN, 'SUPER_ADMIN'),
    (ACCOUNT_ADMIN, 'ACCOUNT_ADMIN'),
    (TECH_ADMIN, 'TECH_ADMIN'),
    (CUSTOMER, 'CUSTOMER'),
)


class UserProfile(models.Model):
    user_type = models.CharField(max_length=1, choices=USER_TYPES,
                                 default=CUSTOMER)
    user = models.OneToOneField(User)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    login_count = models.PositiveIntegerField(default=0)


    def login_user_count(sender, request, user, **kwargs):
        myprofile = user.userprofile
        user_count = myprofile.login_count
        user_count = user_count + 1
        myprofile.login_count = user_count
        myprofile.save()