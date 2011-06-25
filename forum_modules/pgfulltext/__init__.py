from forum.base import get_database_engine
database_type = get_database_engine()

NAME = 'Postgresql Full Text Search'
DESCRIPTION = "Enables PostgreSql full text search functionality."

try:
    import psycopg2
    CAN_USE = 'postgresql' in database_type
except:
    CAN_USE = False
