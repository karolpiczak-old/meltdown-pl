import hashlib
from time import time
from datetime import datetime
from urllib import urlopen,  urlencode
from urlparse import parse_qs
from forum.authentication.base import AuthenticationConsumer, ConsumerTemplateContext, InvalidAuthentication
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode

import settings

try:
    from json import load as load_json
except:
    from django.utils.simplejson import JSONDecoder

    def load_json(json):
        decoder = JSONDecoder()
        return decoder.decode(json.read())

class FacebookAuthConsumer(AuthenticationConsumer):
    
    def process_authentication_request(self, request):
        API_KEY = str(settings.FB_API_KEY)

        # Check if the Facebook cookie has been received.
        if 'fbs_%s' % API_KEY in request.COOKIES:
            fbs_cookie = request.COOKIES['fbs_%s' % API_KEY]
            parsed_fbs = parse_qs(smart_unicode(fbs_cookie))
            self.parsed_fbs = parsed_fbs

            # Check if the session hasn't expired.
            if self.check_session_expiry(request.COOKIES):
                return parsed_fbs['uid'][0]
            else:
                raise InvalidAuthentication(_('Sorry, your Facebook session has expired, please try again'))
        else:
            raise InvalidAuthentication(_('The authentication with Facebook connect failed, cannot find authentication tokens'))
    def check_session_expiry(self, cookies):
        return datetime.fromtimestamp(float(self.parsed_fbs['expires'][0])) > datetime.now()

    def get_user_data(self, cookies):
        API_KEY = str(settings.FB_API_KEY)
        fbs_cookie = cookies['fbs_%s' % API_KEY]
        parsed_fbs = parse_qs(smart_unicode(fbs_cookie))

        # Communicate with the access token to the Facebook oauth interface.
        json = load_json(urlopen('https://graph.facebook.com/me?access_token=%s' % parsed_fbs['access_token'][0]))

        # Return the user data.
        return {
            'username': '%s %s' % (smart_unicode(json['first_name']), smart_unicode(json['last_name'])),
            'email': smart_unicode(json['email']),
        }

class FacebookAuthContext(ConsumerTemplateContext):
    mode = 'BIGICON'
    type = 'CUSTOM'
    weight = 100
    human_name = 'Facebook'
    code_template = 'modules/facebookauth/button.html'
    extra_css = ["http://www.facebook.com/css/connect/connect_button.css"]

    API_KEY = settings.FB_API_KEY