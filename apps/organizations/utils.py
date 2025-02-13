from mayan.apps.views.http import URL

from .settings import setting_organization_installation_url


def get_organization_installation_re_path(request=None):
    result = setting_organization_installation_url.value
    if not result and request:
        result = re_path(
            netloc=request.get_host(), port=request.get_port(),
            scheme=request.scheme
        ).to_string()

    return result
