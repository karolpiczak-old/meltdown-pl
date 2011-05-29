from forum.settings import EXT_KEYS_SET
from forum.settings.base import Setting
from django.utils.translation import ugettext_lazy as _

TWITTER_CONSUMER_KEY = Setting('TWITTER_CONSUMER_KEY', '', EXT_KEYS_SET, dict(
label = _("Twitter consumer key"),
help_text = _("""
Get this key at the <a href="http://twitter.com/apps/">Twitter apps</a> to enable
authentication in your site through Twitter.
"""),
required=False))

TWITTER_CONSUMER_SECRET = Setting('TWITTER_CONSUMER_SECRET', '', EXT_KEYS_SET, dict(
label = _("Twitter consumer secret"),
help_text = _("""
This your Twitter consumer secret that you'll get in the same place as the consumer key.
"""),
required=False))

TWITTER_AUTO_CALLBACK_REDIRECT = Setting('TWITTER_AUTO_CALLBACK_REDIRECT', True, EXT_KEYS_SET, dict(
label = _("Twitter auto-callback redirect"),
help_text = _("""
Automatically redirect to the Twitter authentication done page, pass the oauth_callback parameter.
"""),
required=False))
