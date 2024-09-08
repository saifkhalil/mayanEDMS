from django.utils.translation import gettext_lazy as _

from .classes import CredentialBackend


class CredentialBackendAccessToken(CredentialBackend):
    form_field_widgets = {
        'token': {
            'class': 'django.forms.widgets.PasswordInput',
            'kwargs': {
                'render_value': True
            }
        }
    }
    form_fields = {
        'token': {
            'label': _(message='Token'),
            'class': 'django.forms.CharField', 'default': '',
            'help_text': _(
                'Generated token value used to make API calls.'
            ), 'kwargs': {
                'max_length': 255
            }, 'required': True
        }
    }
    label = _(message='Access token')

    @classmethod
    def get_form_fieldsets(cls):
        fieldsets = super().get_form_fieldsets()

        fieldsets += (
            (
                _(message='Identity'), {
                    'fields': ('token',)
                }
            ),
        )

        return fieldsets


class CredentialBackendGoogleServiceAccount(CredentialBackend):
    form_field_order = (
        'project_id', 'private_key_id', 'private_key', 'client_email',
        'client_id', 'auth_uri', 'token_uri', 'auth_provider_x509_cert_url',
        'client_x509_cert_url'
    )
    form_field_widgets = {
        'private_key': {
            'class': 'django.forms.widgets.Textarea'
        }
    }
    form_fields = {
        'project_id': {
            'label': _('Project ID'),
            'class': 'django.forms.CharField', 'default': '',
            'kwargs': {
                'max_length': 254
            }, 'required': True
        },
        'private_key_id': {
            'label': _('Private Key ID'),
            'class': 'django.forms.CharField', 'default': '',
            'kwargs': {
                'max_length': 254
            }, 'required': True
        },
        'private_key': {
            'label': _('Private Key'),
            'class': 'django.forms.CharField', 'default': ''
        },
        'client_email': {
            'label': _('Client email'),
            'class': 'django.forms.CharField', 'default': '',
            'kwargs': {
                'max_length': 254
            }, 'required': True
        },
        'client_id': {
            'label': _('Client ID'),
            'class': 'django.forms.CharField', 'default': '',
            'kwargs': {
                'max_length': 254
            }, 'required': True
        },
        'auth_uri': {
            'label': _('Authentication URI'),
            'class': 'django.forms.CharField', 'default': 'https://accounts.google.com/o/oauth2/auth',
            'kwargs': {
                'max_length': 254
            }, 'required': True
        },
        'token_uri': {
            'label': _('Token URI'),
            'class': 'django.forms.CharField', 'default': 'https://oauth2.googleapis.com/token',
            'kwargs': {
                'max_length': 254
            }, 'required': True
        },
        'auth_provider_x509_cert_url': {
            'label': _('X509 certificate provider URL'),
            'class': 'django.forms.CharField', 'default': 'https://www.googleapis.com/oauth2/v1/certs',
            'kwargs': {
                'max_length': 254
            }, 'required': True
        },
        'client_x509_cert_url': {
            'label': _('Client X509 certificate URL'),
            'class': 'django.forms.CharField', 'default': '',
            'kwargs': {
                'max_length': 254
            }, 'required': True
        }
    }
    label = _('Google Service Account')

    @classmethod
    def get_form_fieldsets(cls):
        fieldsets = super().get_form_fieldsets()

        fieldsets += (
            (
                _('Project'), {
                    'fields': ('project_id',)
                }
            ),
            (
                _('Secrets'), {
                    'fields': ('private_key_id', 'private_key', 'token_uri')
                }
            ),
            (
                _('Indentity'), {
                    'fields': ('client_email', 'client_id', 'auth_uri')
                }
            ),
            (
                _('Certificate'), {
                    'fields': (
                        'auth_provider_x509_cert_url', 'client_x509_cert_url'
                    )
                }
            )
        )

        return fieldsets

    @classmethod
    def post_processing(cls, obj):
        for key, value in obj.items():
            obj[key] = value.replace('\\n', '\n')

        return obj


class CredentialBackendUsernamePassword(CredentialBackend):
    form_field_widgets = {
        'password': {
            'class': 'django.forms.widgets.PasswordInput',
            'kwargs': {
                'render_value': True
            }
        }
    }
    form_fields = {
        'username': {
            'label': _(message='Username'),
            'class': 'django.forms.CharField', 'default': '',
            'help_text': _(
                'Pseudonym used to identify a user.'
            ), 'kwargs': {
                'max_length': 254
            }, 'required': True
        }, 'password': {
            'label': _(message='Password'),
            'class': 'django.forms.CharField', 'default': '',
            'help_text': _(
                'Character string used to authenticate the user.'
            ), 'kwargs': {
                'max_length': 192
            }, 'required': False
        }
    }
    label = _(message='Username and password')

    @classmethod
    def get_form_fieldsets(cls):
        fieldsets = super().get_form_fieldsets()

        fieldsets += (
            (
                _(message='Identity'), {
                    'fields': ('username', 'password')
                }
            ),
        )

        return fieldsets
