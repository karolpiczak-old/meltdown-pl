NAME = 'Mysql Full Text Search'
DESCRIPTION = "Enables Mysql full text search functionality."

try:
    import MySQLdb
    import settings_local
    CAN_USE = settings_local.DATABASE_ENGINE in ('mysql', 'pooled_mysql')
except Exception, e:
    import traceback
    traceback.print_exc()
    CAN_USE = False
  