from django.db import connection, transaction
import os, settings

import re
from django.db import connection, transaction, models
from django.db.models import Q
from forum.models.question import Question, QuestionManager
from forum.models.node import Node
from forum.modules import decorate

VERSION = 2

f_name = None

if not bool(settings.MYSQL_FTS_INSTALLED):
    f_name = os.path.join(os.path.dirname(__file__), 'fts_install.sql')
elif int(settings.MYSQL_FTS_VERSION < VERSION):
    f_name = os.path.join(os.path.dirname(__file__), 'fts_update.sql')

if f_name:
    f = open(f_name, 'r')

    try:
        cursor = connection.cursor()
        cursor.execute(f.read())
        transaction.commit_unless_managed()

        settings.MYSQL_FTS_INSTALLED.set_value(True)
        settings.MYSQL_FTS_VERSION.set_value(VERSION)

    except Exception, e:
        #import sys, traceback
        #traceback.print_exc(file=sys.stdout)
        pass
    finally:
        cursor.close()

    f.close()

word_re = re.compile(r'\w+', re.UNICODE)

@decorate(QuestionManager.search, needs_origin=False)
def question_search(self, keywords):
    keywords = keywords.upper()

    return '-ranking', self.filter(
            models.Q(ftsindex__body__search=keywords) or models.Q(ftsindex__title__search=keywords) or models.Q(ftsindex__tagnames__search=keywords)

    ).extra(
        select={
            'ranking': """
                match(forum_mysqlftsindex.tagnames) against (%s in boolean mode) * 4 +
                match(forum_mysqlftsindex.title) against (%s in boolean mode) * 2 +
                match(forum_mysqlftsindex.body) against (%s in boolean mode) * 1
                                """,
            },
        select_params=[keywords, keywords, keywords]
    )
