import os.path
from base import Setting, SettingSet, BaseSetting

from django.forms.widgets import Textarea
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as djsettings
from django.utils.version import get_svn_revision

from forum.modules import get_modules_script_implementations

OSQA_VERSION = "Development Build"

SVN_REVISION = get_svn_revision(djsettings.SITE_SRC_ROOT)

# We'll have to keep in mind this variable on every release.
if SVN_REVISION == u'SVN-unknown':
    SVN_REVISION = u'SVN-1000'

MAINTAINANCE_MODE = Setting('MAINTAINANCE_MODE', None)

SETTINGS_PACK = Setting('SETTINGS_PACK', "default")
DJSTYLE_ADMIN_INTERFACE = Setting('DJSTYLE_ADMIN_INTERFACE', True)
NODE_MAN_FILTERS = Setting('NODE_MAN_FILTERS', [])

APP_URL = djsettings.APP_URL
APP_BASE_URL = djsettings.APP_BASE_URL
FORCE_SCRIPT_NAME = djsettings.FORCE_SCRIPT_NAME
OSQA_SKIN = djsettings.OSQA_DEFAULT_SKIN
LANGUAGE_CODE = djsettings.LANGUAGE_CODE
ADMIN_MEDIA_PREFIX = djsettings.ADMIN_MEDIA_PREFIX
ONLINE_USERS = Setting('ONLINE_USERS', {})


from basic import *
from sidebar import *
from email import *
from extkeys import *
from minrep import *
from repgain import *
from voting import *
from upload import *
from about import *
from faq import *
from form import *
from view import *
from moderation import *
from users import *
from static import *
from urls import *
from accept import *
from sitemaps import *

__all__ = locals().keys()

# Be able to import all module settings as well
for k,v in get_modules_script_implementations('settings', BaseSetting).items():
   if not k in __all__:
        __all__.append(k)
        exec "%s = v" % k


BADGES_SET = SettingSet('badges', _('Badges config'), _("Configure badges on your OSQA site."), 500)


