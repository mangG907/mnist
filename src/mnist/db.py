import pymysql.cursors

def get_connection():
  connection = pymysql.connect(host='172.18.0.1', port = 43306,
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


