__author__ = 'aamirbhatt'

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
import re
from models import UserProfile

from django.core.mail import EmailMessage


class UserProfileListResource:
    """ Operations related to SuperAdminProfile """

    def _post(self, user_obj, user_type=None):
        """ Create a  userprofile """
        user_profile = UserProfile()
        if user_type:
            user_profile.user_type = user_type
        user_profile.user = user_obj
        user_profile.save()
        return user_profile


class UserInstanceResource:
    def _get(self, id=None, email=None):
        if email:
            return User.objects.get(username=email)
        return User.objects.get(pk=id)

    def _post(self, email, first_name=None, last_name=None, password=None,
              user_type=None):
        user = User()
        user.email = email
        user.username = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if password:
            user.set_password(password)
        user.save()
        if user:
            UserProfileListResource()._post(user_obj=user, user_type=user_type)
        return user


    def _update(self, id, password=None, first_name=None, last_name=None,
                email=None):
        user = User.objects.get(pk=id)
        if password:
            user.set_password(password)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.username = email
            user.email = email
        user.save()
        return user

    def _filter(self,email=None,user_type=None):
        # filter by
        return User.objects.filter(username=email)


    def _sent(self, user, password_reset_url, new_user=None):
        ctx = {
            "user": user,
            "current_site": settings.SITE_DOMAIN,
            "password_reset_url": password_reset_url,
            "newuser": new_user
        }
        subject = render_to_string("email/password_reset_subject.txt", ctx)
        subject = "".join(subject.splitlines())
        message = render_to_string("email/activate_password.html", ctx)
        msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL,
                           [user.email])
        msg.content_subtype = 'html'
        msg.send()


