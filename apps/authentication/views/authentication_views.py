from collections import OrderedDict

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as django_auth_login
)
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView,
    PasswordResetCompleteView, PasswordResetConfirmView,
    PasswordResetDoneView, PasswordResetView, RedirectURLMixin
)
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.urls import reverse, reverse_lazy
from django.utils.decorators import classonlymethod, method_decorator
from django.utils.translation import gettext_lazy as _, ngettext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from formtools.wizard.views import SessionWizardView, StepsHelper
from stronghold.decorators import public
from stronghold.views import StrongholdPublicMixin

import mayan
from mayan.apps.common.settings import setting_home_view
from mayan.apps.forms import formsets
from mayan.apps.organizations.utils import get_organization_installation_url
from mayan.apps.user_management.permissions import permission_user_edit
from mayan.apps.user_management.querysets import (
    get_all_users_queryset, get_user_queryset
)
from mayan.apps.views.generics import MultipleObjectFormActionView
from mayan.apps.views.http import URL
from mayan.apps.views.view_mixins import ViewIconMixin

from ..classes import AuthenticationBackend
from ..forms import AuthenticationFormBase
from ..icons import icon_login, icon_password_change
from ..literals import SESSION_MULTI_FACTOR_USER_ID_KEY
from ..settings import setting_disable_password_reset


class MultiFactorAuthenticationView(RedirectURLMixin, SessionWizardView):
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'authentication/login.html'

    # Login view methods.
    get_default_redirect_url = LoginView.get_default_redirect_url
    get_redirect_url = LoginView.get_redirect_url
    get_success_url = LoginView.get_success_url

    @staticmethod
    def condition_dict(self):
        self.authentication_backend = AuthenticationBackend.cls_get_instance()
        condition_dict = self.authentication_backend.get_condition_dict()
        return condition_dict

    @staticmethod
    def form_list_property(self):
        """
        Return the processed form list after the view has initialized.
        """
        self.authentication_backend = AuthenticationBackend.cls_get_instance()
        form_list = self.authentication_backend.get_form_list()
        computed_form_list = OrderedDict()

        for form_index, form in enumerate(iterable=form_list):
            computed_form_list[
                str(form_index)
            ] = form

        for form in computed_form_list.values():
            if issubclass(form, formsets.BaseFormSet):
                form = form.form

        return computed_form_list

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        # `SessionWizardView` needs at least one form in order to be
        # initialized as a view. Declare one empty form and then change the
        # form list in the `.dispatch()` method.
        class EmptyForm(AuthenticationFormBase):
            """Empty form"""

        cls.form_list = [EmptyForm]

        # Allow super to initialize and pass the `form_list` `len()` assert
        # before replacing the `form_list` attribute with our property.
        result = super().as_view(*args, **kwargs)

        def null_setter(self, value):
            return

        cls.form_list = property(
            fget=MultiFactorAuthenticationView.form_list_property,
            fset=null_setter
        )
        cls.condition_dict = property(
            fget=MultiFactorAuthenticationView.condition_dict,
            fset=null_setter
        )

        return result

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    @method_decorator(public)
    def dispatch(self, request, *args, **kwargs):
        steps = StepsHelper(self)

        if steps.count == 0:
            user_id = request.session.get(
                SESSION_MULTI_FACTOR_USER_ID_KEY, None
            )
            if user_id:
                return self.done()
            else:
                return HttpResponseRedirect(
                    redirect_to=resolve_url(
                        to=settings.LOGIN_URL
                    )
                )
        else:
            return super().dispatch(request=request, *args, **kwargs)

    def done(self, form_list=None, **kwargs):
        """
        Perform the same function as Django's `LoginView.form_valid()`.
        """
        kwargs = self.get_all_cleaned_data()
        self.authentication_backend.process(
            form_list=form_list, kwargs=kwargs, request=self.request
        )
        user = self.authentication_backend.get_user(
            form_list=form_list, kwargs=kwargs, request=self.request
        )

        django_auth_login(request=self.request, user=user)

        return HttpResponseRedirect(
            redirect_to=self.get_success_url()
        )

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        context.update(
            AuthenticationBackend.cls_get_instance().get_context_data()
        )

        wizard_step = self.form_list[self.steps.current]

        if self.storage.current_step == self.steps.last:
            context['submit_label'] = None
        else:
            context['submit_label'] = _(message='Next')

        context.update(
            {
                'form_css_classes': 'form-hotkey-double-click',
                'step_title': _(
                    message='Step %(step)d of %(total_steps)d: '
                    '%(step_label)s'
                ) % {
                    'step': self.steps.step1,
                    'step_label': wizard_step._label,
                    'total_steps': len(self.form_list)
                },
                'wizard_step': wizard_step,
                'wizard_steps': self.form_list
            }
        )
        return context

    def get_form_kwargs(self, step):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['wizard'] = self
        return kwargs


class MayanLoginView(StrongholdPublicMixin, LoginView):
    extra_context = {
        'appearance_type': 'plain',
        'submit_icon': icon_login,
        'submit_label': _(message='Sign in')
    }
    redirect_authenticated_user = True
    template_name = 'authentication/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            AuthenticationBackend.cls_get_instance().get_context_data()
        )
        return context

    def get_form_class(self):
        return AuthenticationBackend.cls_get_instance().get_login_form_class()

    def form_valid(self, form):
        if not AuthenticationBackend.cls_get_instance().form_list:
            AuthenticationBackend.cls_get_instance().process(
                kwargs=form.cleaned_data, request=self.request

            )
            return super().form_valid(form=form)
        else:
            self.request.session[
                SESSION_MULTI_FACTOR_USER_ID_KEY
            ] = form.get_user().pk

            url = URL(
                path=reverse(
                    viewname='authentication:multi_factor_authentication_view'
                )
            )

            next_url = self.get_redirect_url()
            if next_url:
                url.args[self.redirect_field_name] = next_url

            return HttpResponseRedirect(
                redirect_to=url.to_string()
            )


class MayanLogoutView(LogoutView):
    """No current change or overrides, left here for future expansion."""


class MayanPasswordChangeDoneView(PasswordChangeDoneView):
    def dispatch(self, *args, **kwargs):
        messages.success(
            message=_(
                message='Your password has been successfully changed.'
            ),
            request=self.request
        )
        return redirect(
            to=self.request.user.get_absolute_url()
        )


class MayanPasswordChangeView(ViewIconMixin, PasswordChangeView):
    extra_context = {
        'title': _(message='Current user password change')
    }
    success_url = reverse_lazy(
        viewname='authentication:password_change_done'
    )
    template_name = 'appearance/form_container.html'
    view_icon = icon_password_change

    def dispatch(self, *args, **kwargs):
        if self.request.user.user_options.block_password_change:
            messages.error(
                message=_(
                    message='Changing the password is not allowed for '
                    'this account.'
                ), request=self.request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(viewname=setting_home_view.view)
            )

        return super().dispatch(*args, **kwargs)


class MayanPasswordResetCompleteView(
    StrongholdPublicMixin, PasswordResetCompleteView
):
    extra_context = {
        'appearance_type': 'plain'
    }
    template_name = 'authentication/password_reset_complete.html'


class MayanPasswordResetConfirmView(
    StrongholdPublicMixin, PasswordResetConfirmView
):
    extra_context = {
        'appearance_type': 'plain'
    }
    success_url = reverse_lazy(
        viewname='authentication:password_reset_complete_view'
    )
    template_name = 'authentication/password_reset_confirm.html'


class MayanPasswordResetDoneView(
    StrongholdPublicMixin, PasswordResetDoneView
):
    extra_context = {
        'appearance_type': 'plain'
    }
    template_name = 'authentication/password_reset_done.html'


class MayanPasswordResetView(StrongholdPublicMixin, PasswordResetView):
    email_template_name = 'authentication/password_reset_email.html'
    extra_context = {
        'appearance_type': 'plain'
    }
    subject_template_name = 'authentication/password_reset_subject.txt'
    success_url = reverse_lazy(
        viewname='authentication:password_reset_done_view'
    )
    template_name = 'authentication/password_reset_form.html'

    # Hardcoded overloaded method to allow adding extra email context from
    # a method and not just the Django provided `self.extra_email_context`.
    # On each new Django version, verify if this method has changed and
    # update this overloading.
    def form_valid(self, form):
        opts = {
            'email_template_name': self.email_template_name,
            'extra_email_context': self.get_extra_email_context(),
            'from_email': self.from_email,
            'html_email_template_name': self.html_email_template_name,
            'request': self.request,
            'subject_template_name': self.subject_template_name,
            'token_generator': self.token_generator,
            'use_https': self.request.is_secure()
        }
        form.save(**opts)
        # Specify the super class `PasswordResetView` explicitly to avoid
        # executing `form_valid` again.
        return super(PasswordResetView, self).form_valid(form=form)

    def get(self, *args, **kwargs):
        if setting_disable_password_reset.value:
            return redirect(to=setting_home_view.value)
        return super().get(*args, **kwargs)

    def get_extra_email_context(self):
        extra_email_context_project_website = get_organization_installation_url(
            request=self.request
        )
        extra_email_context = {
            'project_copyright': mayan.__copyright__,
            'project_license': mayan.__license__,
            'project_title': mayan.__title__,
            'project_website': str(extra_email_context_project_website)
        }
        return extra_email_context

    def post(self, *args, **kwargs):
        if setting_disable_password_reset.value:
            return redirect(to=setting_home_view.value)
        return super().post(*args, **kwargs)


class UserSetPasswordView(MultipleObjectFormActionView):
    form_class = SetPasswordForm
    object_permission = permission_user_edit
    pk_url_kwarg = 'user_id'
    source_queryset = get_user_queryset()
    success_message = _(
        message='Password change request performed on %(count)d user'
    )
    success_message_plural = _(
        message='Password change request performed on %(count)d users'
    )
    view_icon = icon_password_change

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request=request, *args, **kwargs)

        queryset = self.get_queryset(
            source_queryset=get_all_users_queryset()
        )

        queryset_staff_users = queryset.filter(is_staff=True)
        queryset_super_users = queryset.filter(is_superuser=True)

        if queryset_staff_users.exists() or queryset_super_users.exists():
            messages.warning(
                message=_(
                    message='Changing the password of staff or super user '
                    'accounts via the user interface is not allowed. '
                    'Use administration tools to perform this '
                    'operation.'
                ), request=self.request
            )

        return result

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ngettext(
                singular='Change user password',
                plural='Change users passwords',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        message='Change password for user: %s'
                    ) % queryset.first()
                }
            )

        return result

    def get_form_extra_kwargs(self):
        queryset = self.object_list
        result = {}
        if queryset:
            result['user'] = queryset.first()
            return result
        else:
            raise PermissionDenied

    def object_action(self, form, instance):
        try:
            instance.set_password(
                raw_password=form.cleaned_data['new_password1']
            )
            instance.save()
            messages.success(
                message=_(
                    message='Successful password reset for user: %s.'
                ) % instance, request=self.request
            )
        except Exception as exception:
            messages.error(
                message=_(
                    message='Error resetting password for user '
                    '"%(user)s": %(error)s'
                ) % {
                    'error': exception, 'user': instance
                }, request=self.request
            )
