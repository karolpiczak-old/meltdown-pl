from django.conf import settings as django_settings

def get_database_engine():
    try:
        database_type = django_settings.DATABASE_ENGINE

        if len(database_type) == 0:
            raise Exception('Empty old style database engine')
    except:
        try:
            database_type = django_settings.DATABASES['default']['ENGINE']
        except:
            database_type = 'unknown'

    return str(database_type)