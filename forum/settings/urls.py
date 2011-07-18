from base import Setting, SettingSet
from django.utils.translation import ugettext as _

URLS_SET = SettingSet('urls', _('URL settings'), _("Some settings to tweak behaviour of site urls (experimental)."))

INCLUDE_ID_IN_USER_URLS = Setting('INCLUDE_ID_IN_USER_URLS', True, URLS_SET, dict(
label = _("Include IDs in user URLs"),
help_text = _("Choose this if you want to have IDs included in the user-related URLs."),
required=False))

ALLOW_UNICODE_IN_SLUGS = Setting('ALLOW_UNICODE_IN_SLUGS', False, URLS_SET, dict(
label = _("Allow unicode in slugs"),
help_text = _("Allow unicode/non-latin characters in urls."),
required=False))

FORCE_SINGLE_URL = Setting('FORCE_SINGLE_URL', True, URLS_SET, dict(
label = _("Force single url"),
help_text = _("Redirect the request in case there is a mismatch between the slug in the url and the actual slug"),
required=False))

