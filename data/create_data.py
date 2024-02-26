from dotenv import load_dotenv
import os.path
import sqlite3 as sql
import bcrypt 

#Loading user info from .env file =>
load_dotenv()
username = os.getenv("username")
teamname = os.getenv("teamname")
email = os.getenv("email")
name = os.getenv("name")
job = os.getenv("job")
password = os.getenv("password")

#bcrypt the password =>
bytes = password.encode('utf-8') 
salt = bcrypt.gensalt() 
hash = bcrypt.hashpw(bytes, salt) 

#connect to database
con = sql.connect("User.db")
c = con.cursor()

#creating user table =>
c.execute(""" CREATE TABLE IF NOT EXISTS USERS(id integer primary key AUTOINCREMENT, username TEXT VARCHAR(20) UNIQUE,
           TeamName TEXT VARCHAR(30) UNIQUE, email TEXT VARCHAR(20) UNIQUE, name TEXT VARCHAR(30), job TEXT VARCHAR(20), password TEXT, isAdmin BOOLEAN)""")

c.execute("""INSERT INTO USERS(username, TeamName, email, name, job, password, isAdmin) VALUES("{}", "{}", "{}", "{}", "{}", "{}", {});""".format(username, teamname, email, name, job, hash, True))
con.commit()