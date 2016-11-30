import sqlite3

DB = 'var/forum.db'
conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute("DROP TABLE if EXISTS worker")
cursor.execute("DROP TABLE if EXISTS user")
cursor.execute("DROP TABLE if EXISTS department")
cursor.execute("DROP TABLE if EXISTS intership")

cursor.execute("""CREATE TABLE user
               (id INTEGER PRIMARY KEY AUTOINCREMENT, login text, password text)
               """)
			   
cursor.execute("""CREATE TABLE department
               (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, location text)
               """)
               
cursor.execute("""CREATE TABLE worker
               (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, surname text, post text, dateOfBirth text, email text, department text)
               """)
			   
cursor.execute("""CREATE TABLE intership
               (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, surname text, university text, dateOfBirth text, email text, department text)
               """)

cursor.execute("INSERT INTO user (login, password) VALUES ('manuel', 'hola')")
cursor.execute("INSERT INTO user (login, password) VALUES ('manuel2', 'hola2')")

cursor.execute("INSERT INTO department (name, location) VALUES ('Computers', 'Building 1')")
cursor.execute("INSERT INTO department (name, location) VALUES ('Human Relations', 'Building 2')")


cursor.execute("INSERT INTO worker (name, surname, post, dateOfBirth, email, department) VALUES ('Manuel', 'Martinez', 'Manager', '20/02/1992', 'manu@napier.com','Computers')")
cursor.execute("INSERT INTO worker (name, surname, post, dateOfBirth, email, department) VALUES ('Marcos', 'Perez', 'Worker', '10/03/1993','marcos@napier.com', 'Humans Relations')")

cursor.execute("INSERT INTO intership (name, surname, university, dateOfBirth, email, department) VALUES ('Jhon', 'Martinez', 'UPV', '20/02/1992', 'manu@napier.com', 'Human Relations')")
cursor.execute("INSERT INTO intership (name, surname, university, dateOfBirth, email, department) VALUES ('Charlie', 'Perez', 'Napier', '10/03/1993','marcos@napier.com', 'Computers')")



conn.commit()

print "database created"