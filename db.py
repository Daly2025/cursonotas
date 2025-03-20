import pymysql.cursors

def connect():
    return pymysql.connect(
        host='localhost',
        user='root',  # Cambia esto si usas otro usuario
        password='',  # Cambia esto si tienes contraseña
        database='cursonotas',  # Nombre de tu base de datos
        cursorclass=pymysql.cursors.DictCursor
    )

def query(sql, params=None):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

def query_one(sql, params=None):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

def execute(sql, params=None):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            connection.commit()