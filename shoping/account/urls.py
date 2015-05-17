from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from views import ChangePasswordResetTokenView
from views import PasswordChangedView
from views import LogoutView
# from views import EditUserView
# from views import PasswordResetTokenView
from dashboard.views import DashBoardView
from views import PasswordResetView
from views import LoginView, PasswordResetTokenView
from views import SignupView

__author__ = 'aamirbhatt'

urlpatterns = patterns("",


    url(r'signup/$', SignupView.as_view(), name='account_signup'),
    url(r'home/$', DashBoardView.as_view(), name='home'),
    url(r'logout/$', LogoutView.as_view(), name="account_logout"),
    # url(r'edit/(?P<user_id>[\-\d\w]+)/$',login_required(EditUserView.as_view()),
    #    name="edit_user"),
    url(r"password/reset/$", PasswordResetView.as_view(),
       name="account_password_reset"),
    # url(r'^activate/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    #    PasswordResetTokenView.as_view(),
    #    name='account_password_reset_token'),
    url(r'^changepassword/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       ChangePasswordResetTokenView.as_view(),
       name='change_password_reset_token'),
    url(r"password/changed/$", PasswordChangedView.as_view(),
       name="account_password_changed"),
    url(r'$', LoginView.as_view(), name='account_login')
)