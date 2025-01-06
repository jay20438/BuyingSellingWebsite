import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database = "endsemeval")

mycursor = mydb.cursor()

mycursor.execute("select * from buyers")

for i in mycursor:
    print(i)
