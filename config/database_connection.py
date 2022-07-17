""" Database connection information

Modify this file according to your needs.
"""

import pymysql

mariadb = {
    'host': 'localhost',
    'user': 'changeme',
    'password': 'changeme',
    'db': 'changeme',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    'sql_file': 'config/create_db.sql'
}
