# -*- coding: utf-8 -*-

import os
import sys
import platform
import bz2
import urllib2, urllib
import binascii
import string
import random
import re
import urllib2
import settings
import datetime
import logging


from xml.dom.minidom import parse, parseString
from forum.base import get_database_engine
from forum.models import Question, Answer, Comment, User
from forum.settings import APP_URL, SVN_REVISION, APP_TITLE, APP_DESCRIPTION
from django import VERSION as DJANGO_VERSION
from django.utils import simplejson
from django.utils.html import escape
from django.utils.encoding import smart_unicode
from django.conf import settings as django_settings
from django.utils.translation import ugettext as _


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

# Gets the active users count since the last visit
def get_active_users():
    users_count = 0

    try:
        if settings.LATEST_UPDATE_DATETIME:
            users_count = User.objects.filter(last_login__gt=settings.LATEST_UPDATE_DATETIME).count()
    except:
        pass

    return users_count

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

def check_for_updates():
    # Get the SVN Revision
    try:
        svn_revision = int(SVN_REVISION.replace('SVN-', ''))
    except ValueError:
        # Here we'll have to find another way of getting the SVN revision
        svn_revision = 0

    admin_emails_xml = '<emails>'
    for email in get_admin_emails():
        admin_emails_xml += '<email value="%s" />' % email
    admin_emails_xml += '</emails>'

    database_type = get_database_engine()

    statistics = u"""<check>
    <key value="%(site_key)s" />
    <app_url value="%(app_url)s" />
    <app_title value="%(app_title)s" />
    <app_description value="%(app_description)s" />
    <svn_revision value="%(svn_revision)d" />
    <views value="%(site_views)d" />
    <questions_count value="%(questions_count)d" />
    <answers_count value="%(answers_count)d" />
    <comments_count value="%(comments_count)d" />
    <active_users value="%(active_users)d" />
    <server value="%(server_name)s" />
    <python_version value="%(python_version)s" />
    <django_version value="%(django_version)s" />
    <database value="%(database)s" />
    <os value="%(os)s" />
    %(emails)s
</check> """ % {
        'site_key' : settings.SITE_KEY,
        'app_url' : APP_URL,
        'app_title' : escape(APP_TITLE.value),
        'app_description' : escape(APP_DESCRIPTION.value),
        'svn_revision' : svn_revision,
        'site_views' : get_site_views(),
        'server_name' : get_server_name(),
        'questions_count' : Question.objects.filter_state(deleted=False).count(),
        'answers_count' : Answer.objects.filter_state(deleted=False).count(),
        'comments_count' : Comment.objects.filter_state(deleted=False).count(),
        'active_users' : get_active_users(),
        'python_version' : ''.join(sys.version.splitlines()),
        'django_version' : str(DJANGO_VERSION),
        'database' : database_type,
        'os' : str(platform.uname()),
        'emails' : admin_emails_xml,
    }

    # Compress the statistics XML dump
    statistics = statistics.encode('ascii', 'xmlcharrefreplace')
    statistics_compressed = bz2.compress(statistics)

    # Pass the compressed statistics to the update server
    post_data = {
        'statistics' : binascii.b2a_base64(statistics_compressed),
    }
    data = urllib.urlencode(post_data)

    # We simulate some browser, otherwise the server can return 403 response
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/5'
    headers={ 'User-Agent' : user_agent,}

    try:
        check_request = urllib2.Request('%s%s' % (settings.UPDATE_SERVER_URL, '/site_check/'), data, headers=headers)
        check_response = urllib2.urlopen(check_request)
        content = check_response.read()
    except urllib2.HTTPError, error:
        content = error.read()
    except:
        return _("Wasn't able to check to the update server.")

    # Read the messages from the Update Server
    try:
        messages_xml_url = '%s%s' % (settings.UPDATE_SERVER_URL, '/messages/xml/')
        messages_request = urllib2.Request(messages_xml_url, headers=headers)
        messages_response = urllib2.urlopen(messages_request)
        messages_xml = messages_response.read()
    except:
        return _("Wasn't able to retreive the update messages.")

    # Store the messages XML in a Setting object
    settings.UPDATE_MESSAGES_XML.set_value(messages_xml)

    messages_dom = parseString(messages_xml)
    messages_count = len(messages_dom.getElementsByTagName('message'))

    # Set the latest update datetime to now.
    now = datetime.datetime.now()
    settings.LATEST_UPDATE_DATETIME.set_value(now)

    return _('%d update messages have been downloaded.') % messages_count

def update_trigger():
    # Trigger the update process
    now = datetime.datetime.now()
    if (now - settings.LATEST_UPDATE_DATETIME) > datetime.timedelta(days=1):
        try:
            update_status = check_for_updates()
            logging.log(logging.INFO, smart_unicode("Update process has been triggered: %s" % update_status))
        except Exception, e:
            logging.errror(smart_unicode(e))
        finally:
            settings.LATEST_UPDATE_DATETIME.set_value(now)
