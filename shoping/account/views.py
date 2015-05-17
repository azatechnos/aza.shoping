from django.contrib.auth.forms import PasswordResetForm
from api import UserInstanceResource
from models import CUSTOMER
from models import TECH_ADMIN
from models import ACCOUNT_ADMIN
from models import SUPER_ADMIN
import signals
from utils import default_redirect

__author__ = 'aamirbhatt'
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36, base36_to_int
from django.views.generic import TemplateView, View, FormView

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext, loader
from django.http import HttpResponse, request
from forms import LoginForm, PasswordResetTokenForm
from forms import LoginForm
from forms import LoginForm
from forms import LoginForm
from forms import UserEditForm
from forms import SignUpForm
from forms import LoginForm



# Create your views here.


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        """
            Renders Index Page with Login Form for unauthenticated user
        where as  authenticated user are returned to Dashboard
        :param request:
        :param args:
        :param kwargs:
        :returns: HttpResponse,HttpResponseRedirect
        """
        if request.user.is_authenticated():
            if request.user.userprofile.user_type == CUSTOMER:
                return HttpResponseRedirect(reverse('home'))

            return HttpResponseRedirect('/user/dashboard')

        context = {'form': self.form_class()}
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        """
            Validates the username and password if credentials are valid
        the user will be  authenticated  and will be returned to Dashboard
        else appropriate message will be displayed to User on the same login page
        :param request:
        :param args:
        :param kwargs:
        :returns: HttpResponse,HttpResponseRedirect
        """

        data = request.POST.copy()
        form = self.form_class(data)
        context = {}
        context['messages'] = []
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)

                    next = request.GET.get('next', None)

                    if next:
                        return HttpResponseRedirect(next)
                    if user.userprofile.user_type == CUSTOMER:
                        return HttpResponseRedirect(reverse('home'))
                    if user.userprofile.user_type == TECH_ADMIN:
                        return HttpResponseRedirect(reverse('home'))
                    if user.userprofile.user_type == ACCOUNT_ADMIN:
                        return HttpResponseRedirect(reverse('home'))
                    if user.userprofile.user_type == SUPER_ADMIN:
                        return HttpResponseRedirect(reverse('home'))
                    return HttpResponseRedirect("/user/dashboard")
                else:

                    messages.error(request, 'Invalid Username or Password',
                                   extra_tags='alert-error')
                    context['form'] = form
                    return self.render_to_response(context)
            except User.DoesNotExist:
                messages.error(request, 'Invalid Username or Password',
                               extra_tags='alert-error')
                # context['message'] = 'Invalid Username or Password'
                context['form'] = form
                return self.render_to_response(context)

        messages.error(request, 'Invalid Username or Password',
                       extra_tags='alert-error')

        context['form'] = form
        return self.render_to_response(context)


class SignupView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    token_generator = default_token_generator

    def make_token(self, user):
        return self.token_generator.make_token(user)


    def get(self, request):
        context = {'form': self.form_class()}
        return self.render_to_response(context)

    def post(self, request):
        data = request.POST
        form = self.form_class(data)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = UserInstanceResource()._post(email=email,
                                                         password = password
                                                         )
            uid = int_to_base36(user.id)
            token = self.make_token(user)
            # activation_link = 'http://' + settings.SITE_DOMAIN + reverse(
            #     'account_password_reset_token',
            #     kwargs=dict(uidb36=uid, token=token))
            # UserInstanceResource()._sent(user=user,password_reset_url=activation_link,
            #                                           new_user=True)
            # insert dashboard link for user
            messages.add_message(request, messages.INFO,
                                 'User Created Successfully')
            return HttpResponseRedirect(reverse('home'))

        context = {'form': form}
        return self.render_to_response(context)

        # class EditUserView(FormView):
        # form_class = UserEditForm
        #     template_name = "signup.html"
        #     def get(self, request, *args, **kwargs):
        #         user_id = kwargs.get('user_id', '')
        #         user_obj=UserInstanceResource()._get(id=user_id)
        #         initial = {'first_name':user_obj.first_name,'last_name':user_obj.last_name,'email':user_obj.email}
        #
        #
        #         form = self.form_class(initial=initial)
        #         context = {'form':form,'user_id': user_id}
        #         return self.render_to_response(context)
        #
        #     def post(self, request, *args, **kwargs):
        #         data = request.POST.copy()
        #         user_id = kwargs.get('user_id', '')
        #         form = self.form_class(data)
        #         if form.is_valid():
        #             first_name = form.cleaned_data['first_name']
        #             last_name = form.cleaned_data['last_name']
        #             password = form.cleaned_data['password']
        #             UserInstanceResource()._update(user_id,first_name=first_name,last_name=last_name,password=password)
        #             messages.add_message(request, messages.INFO, 'Edit Done Successfully')
        #             return HttpResponseRedirect(reverse('admin_dashboard'))
        #         context = {'form':form,'user_id': user_id}
        #         return self.render_to_response(context)
        #
        #
class PasswordResetTokenView(FormView):
    '''
    link from email  has a change password form
    where user changes his password
    if token is valid change form is given
    if not valid token then invalid token is retrived
     '''
    template_name = "signup_token.html"
    template_name_fail = "signup_token_fail.html"
    form_class = PasswordResetTokenForm
    token_generator = default_token_generator
    redirect_field_name = "next"
    messages = {
        "password_changed": {
            "level": messages.SUCCESS,
            "text": "Password successfully changed."
        },
    }

    def get(self, request, **kwargs):
        '''password change form if valid token'''
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ctx = self.get_context_data(form=form)
        if not self.check_token(self.get_user(),
                                self.kwargs["token"]):
            return self.token_fail()
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        ctx = kwargs
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "uidb36": self.kwargs["uidb36"],
            "token": self.kwargs["token"],
            "iuser": self.get_user(),
            "redirect_field_name": redirect_field_name,
            "redirect_field_value":
                self.request.REQUEST.get(redirect_field_name),
        })
        return ctx

    def change_password(self, form):
        user = self.get_user()
        user.set_password(form.cleaned_data["password"])
        user.save()

    def after_change_password(self):
        user = self.get_user()
        signals.password_changed.send(sender=PasswordResetTokenView, user=user)
        if self.messages.get("password_changed"):
            messages.add_message(
                self.request,
                self.messages["password_changed"]["level"],
                self.messages["password_changed"]["text"]
            )

    def form_valid(self, form):
        self.change_password(form)
        self.after_change_password()
        return redirect(self.get_success_url())

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings. \
                ACCOUNT_PASSWORD_RESET_REDIRECT_URL
        kwargs.setdefault("redirect_field_name",
                          self.get_redirect_field_name())
        return default_redirect(self.request,
                                fallback_url, **kwargs)

    def get_user(self):
        try:
            uid_int = base36_to_int(self.kwargs["uidb36"])
        except ValueError:
            raise Http404()
        return get_object_or_404(User, id=uid_int)

    def check_token(self, user, token):
        return self.token_generator.check_token(user, token)

    def token_fail(self):
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_fail,
            "context": self.get_context_data()
        }
        return self.response_class(**response_kwargs)

class LogoutView(View):
    '''base class for logout'''

    def get(self, *args, **kwargs):
        '''authenticated users are returned back to index page'''
        if self.request.user.is_authenticated():
            logout(self.request)
        return HttpResponseRedirect(reverse('account_login'))
        #
class PasswordResetView(FormView):
    '''forgot password
     registered email is given and sents link to your registered email'''
    template_name = "account/password_reset.html"
    template_name_sent = "account/password_reset_sent.html"
    form_class = PasswordResetForm
    token_generator = default_token_generator

    def get_context_data(self, **kwargs):
        '''form with email field is returned'''
        context = kwargs
        if self.request.method == "POST" and "resend" in self.request.POST:
            context["resend"] = True
        return context

    def form_valid(self, form):
        self.send_email(form.cleaned_data["email"])
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_sent,
            "context": self.get_context_data(form=form)
        }
        return self.response_class(**response_kwargs)

    def send_email(self, email):
        '''
         reset link is send to requesting users email
         which is already in our database
         '''
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        #current_site = get_current_site(self.request)
        site_domain = getattr(settings, "SITE_DOMAIN", "localhost")
        for user in User.objects. \
            filter(email__iexact=email):
            uid = int_to_base36(user.id)
            token = self.make_token(user)
            password_reset_url = \
                "{0}://{1}{2}".format(
                    protocol,
                    site_domain,
                    reverse("change_password_reset_token",
                            kwargs=dict(uidb36=uid, token=token))
                )
            UserInstanceResource()._sent(user=user,password_reset_url=password_reset_url)


    def make_token(self, user):
        return self.token_generator.make_token(user)
        #
class PasswordChangedView(TemplateView):
    template_name = "password_changed.html"


class ChangePasswordResetTokenView(FormView):
    '''
    link from email  has a change password form
    where user changes his password
    if token is valid change form is given
    if not valid token then invalid token is retrived
     '''
    template_name = "forgot_token.html"
    template_name_fail = "forgot_token_fail.html"
    form_class = PasswordResetTokenForm
    token_generator = default_token_generator
    redirect_field_name = "next"
    messages = {
        "password_changed": {
            "level": messages.SUCCESS,
            "text": "Password successfully changed."
        },
    }

    def get(self, request, **kwargs):
        '''password change form if valid token'''
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ctx = self.get_context_data(form=form)
        if not self.check_token(self.get_user(),
                                self.kwargs["token"]):
            return self.token_fail()
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        ctx = kwargs
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "uidb36": self.kwargs["uidb36"],
            "token": self.kwargs["token"],
            "iuser": self.get_user(),
            "redirect_field_name": redirect_field_name,
            "redirect_field_value":
                self.request.REQUEST.get(redirect_field_name),
        })
        return ctx

    def change_password(self, form):
        user = self.get_user()
        user.set_password(form.cleaned_data["password"])
        user.save()

    def after_change_password(self):
        user = self.get_user()
        signals.password_changed.send(sender=PasswordResetTokenView, user=user)
        if self.messages.get("password_changed"):
            messages.add_message(
                self.request,
                self.messages["password_changed"]["level"],
                self.messages["password_changed"]["text"]
            )

    def form_valid(self, form):
        self.change_password(form)
        self.after_change_password()
        return redirect(self.get_success_url())

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings. \
                ACCOUNT_PASSWORD_RESET_REDIRECT_URL
        kwargs.setdefault("redirect_field_name",
                          self.get_redirect_field_name())
        return default_redirect(self.request,
                                fallback_url, **kwargs)

    def get_user(self):
        try:
            uid_int = base36_to_int(self.kwargs["uidb36"])
        except ValueError:
            raise Http404()
        return get_object_or_404(User, id=uid_int)

    def check_token(self, user, token):
        return self.token_generator.check_token(user, token)

    def token_fail(self):
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_fail,
            "context": self.get_context_data()
        }
        return self.response_class(**response_kwargs)