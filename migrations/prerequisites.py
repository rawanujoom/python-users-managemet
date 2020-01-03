import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='root', password='root', host="localhost")

cursor = mariadb_connection.cursor()

database = 'resumeManagement'
query = "CREATE DATABASE IF NOT EXISTS {db};".format(db=database)
cursor.execute(query)
mariadb_connection.close()

mariadb_connection = mariadb.connect(host="localhost", user='root', password='root', database=database)
cursor = mariadb_connection.cursor()

query = """CREATE TABLE IF NOT EXISTS applicants (
                           id varchar(250) NOT NULL,
                           first_name varchar(250) NOT NULL,
                           last_name varchar(250) NOT NULL,
                           dob DATE NOT NULL,
                           years_of_experience int(100) NOT NULL,
                           dept_id ENUM('IT','HR','Finance') NOT NULL,
                           path varchar(250) NOT NULL,
                           registration_time DATETIME NOT NULL);"""
cursor.execute(query)
mariadb_connection.close()
