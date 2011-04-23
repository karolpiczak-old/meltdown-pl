import string
import random
import re

import urllib2

from forum.models import Question, User
from forum.settings import APP_URL

def generate_installation_key():
    gen = lambda length: "".join( [random.choice(string.digits+string.letters) for i in xrange(length)])
    return '%s-%s-%s-%s' % (gen(4), gen(4), gen(4), gen(4))

# To get the site views count we get the SUM of all questions views.
def get_site_views():
    views = 0

    # Go through all questions and increase the views count
    for question in Question.objects.all():
        views += question.view_count

    return views

def get_server_name():
    url = '%s/' % APP_URL

    try:
        # Make the request
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

        # Get the response information
        response_info = response.info()

        server_name = re.findall("Server: (?P<server_name>.*)$", str(response_info))[0]
        server_name = ''.join(server_name.splitlines())

        return server_name
    except:
        return 'Unknown'

def get_admin_emails():
    emails = []

    for user in User.objects.filter(is_superuser=True):
        emails.append(user.email)

    return emails