from django.urls import re_path import url

from .views import (
    UserOTPDataDetailView, UserOTPDataDisableView, UserOTPDataEnableView,
    UserOTPDataVerifyTokenView
)


urlpatterns = [
    re_path(
        regex=r'^otp/$', name='otp_detail',
        view=UserOTPDataDetailView.as_view()
    ),
    re_path(
        regex=r'^otp/disable/$', name='otp_disable',
        view=UserOTPDataDisableView.as_view()
    ),
    re_path(
        regex=r'^otp/enable/$', name='otp_enable',
        view=UserOTPDataEnableView.as_view()
    ),
    re_path(
        regex=r'^otp/verify/$', name='otp_verify',
        view=UserOTPDataVerifyTokenView.as_view()
    )
]
