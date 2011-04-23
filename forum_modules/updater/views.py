import os
import sys
import bz2
import urllib2, urllib
import binascii

from xml.dom.minidom import parse, parseString

from django import VERSION as DJANGO_VERSION
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.conf import settings

from base import get_site_views, get_server_name
from settings import SITE_KEY, UPDATE_SERVER_URL
from forum.settings import APP_URL, SVN_REVISION
from forum.views.admin import admin_tools_page, admin_page

@admin_tools_page(_('updater'), _('Update Checker'))
def updater_index(request):
    return (
        'modules/updater/index.html',
        {

        },
    )

def updater_check(request):
    # Get the SVN Revision
    try:
        svn_revision = int(SVN_REVISION.replace('SVN-', ''))
    except ValueError:
        # Here we'll have to find another way of getting the SVN revision
        svn_revision = 0

    statistics = """<check>
    <key value="%(site_key)s" />
    <app_url value="%(app_url)s" />
    <svn_revision value="%(svn_revision)d" />
    <views value="%(site_views)d" />
    <active_users value="11959" />
    <server value="%(server_name)s" />
    <python_version value="%(python_version)s" />
    <django_version value="%(django_version)s" />
    <database value="%(database)s" />
    <os value="%(os)s" />
</check> """ % {
        'site_key' : SITE_KEY,
        'app_url' : APP_URL,
        'svn_revision' : svn_revision,
        'site_views' : get_site_views(),
        'server_name' : get_server_name(),
        'python_version' : ''.join(sys.version.splitlines()),
        'django_version' : str(DJANGO_VERSION),
        'database' : settings.DATABASE_ENGINE,
        'os' : str(os.uname()),
    }

    # Compress the statistics XML dump
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
        check_request = urllib2.Request('%s%s' % (UPDATE_SERVER_URL, '/site_check/'), data, headers=headers)
        check_response = urllib2.urlopen(check_request)
        content = check_response.read()
    except urllib2.HTTPError, error:
        content = error.read()

    # Read the messages from the Update Server
    messages_xml_url = '%s%s' % (UPDATE_SERVER_URL, '/messages/xml/')
    messages_request = urllib2.Request(messages_xml_url, headers=headers)
    messages_response = urllib2.urlopen(messages_request)
    messages_xml = messages_response.read()

    messages_dom = parseString(messages_xml)
    messages_count = len(messages_dom.getElementsByTagName('message'))

    return HttpResponse(_('%d update messages have been downloaded') % messages_count, mimetype='text/html')