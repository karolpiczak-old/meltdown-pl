from forum.base import get_database_engine
database_type = get_database_engine()

NAME = 'Mysql Full Text Search'
DESCRIPTION = "Enables Mysql full text search functionality."

try:
    import MySQLdb
    import settings_local
    CAN_USE = 'mysql' in database_type
except Exception, e:
    import traceback
    traceback.print_exc()
    CAN_USE = False
