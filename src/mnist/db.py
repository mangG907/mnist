import pymysql.cursors
import os

def get_connection():
  connection = pymysql.connect(host=os.getenv("DB_IP", "localhost"),
                            port = int(os.getenv("DB_PORT", "43306")),
                            user = 'mnist', password = '1234',
                            database = 'mnistdb',
                            cursorclass=pymysql.cursors.DictCursor)
  return connection


def select(query: str, size = -1):
  connection = get_connection()
  with connection:
      with connection.cursor() as cursor:
          cursor.execute(query)
          result = cursor.fetchmany(size)

  return result

def dml(sql, *values):
  connection = get_connection()

  with connection:
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
        connection.commit()
        return cursor.rowcount


