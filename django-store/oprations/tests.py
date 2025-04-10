from django.test import TestCase

def reade_db(db_name):
    import openpyxl
    import sqlite3
    sql_connection =sqlite3.connect(db_name)
    sql_commant = """SELECT * FROM order"""

    data = sql_connection.execute(sql_commant)

