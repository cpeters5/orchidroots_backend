from django.conf.urls import url
from .views import *
from rest_framework.authtoken import views as restviews
from django.urls import include, path

app_name = "accounts"
urlpatterns = [
    url(r'^signup/$', Signup.as_view(), name="signup_api"),
    url(r'^logout/', Logout.as_view(), name="logout"),
    url(r'^login/$', Login.as_view(), name="login"),
    url(r'^countries/$', CountryView.as_view(), name="country"),
    url(r'^photographers/$', PhotographerView.as_view(), name="photographer"),
    url(r'^verify-code/$', VerifyEmailCode.as_view(), name='verify_code'),
    url(r'^resend-verify-code/$', ResendVerificationEmail.as_view(), name='resend-verify_code'),

    url(r'^forget-password-send-code/$', ForgetPasswordSendEmailCodeView.as_view(), name='forget_password_send_code'),
    url(r'^forget-password-verify-code/$', ResetPasswordVerifyCodeApi.as_view(), name='forget_password_verify_code'),
    url(r'^reset-password/$', RestPasswordApi.as_view(), name='reset_password'),

    url(r'^social-login/$', SocialLogin.as_view(), name="social_login"),
]
