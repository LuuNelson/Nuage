import psycopg2
import psycopg2.extras

"""
def connect():
  conn = psycopg2.connect(
    dbname = 'harris.abassi_db',
    host = 'sqletud.u-pem.fr',
    password = 'Bestdu75',
    cursor_factory = psycopg2.extras.NamedTupleCursor
  )
  conn.autocommit = True
  return conn
"""


def connect():
  conn = psycopg2.connect( "postgresql://nelson.luu_owner:Da8rlIAW4wFd@ep-shy-heart-a2fqirtc.eu-central-1.aws.neon.tech/nelson.luu?sslmode=require",
                          cursor_factory=psycopg2.extras.NamedTupleCursor ) 
  conn.autocommit = True 
  return conn


# def connect():
#   conn = psycopg2.connect(
#     dbname = 'harris',
#     cursor_factory = psycopg2.extras.NamedTupleCursor
#   )
#   conn.autocommit = True
#   return conn