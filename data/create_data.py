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
purpose = os.getenv("purpose")

#bcrypt the password =>
bytes = password.encode('utf-8') 
salt = bcrypt.gensalt() 
hash = bcrypt.hashpw(bytes, salt) 

#connect to database
con = sql.connect("User.db")
c = con.cursor()

#creating user table =>
c.execute(""" CREATE TABLE IF NOT EXISTS USERS(id integer primary key AUTOINCREMENT, username TEXT VARCHAR(20) UNIQUE,
           TeamName TEXT VARCHAR(30), email TEXT VARCHAR(20) UNIQUE, name TEXT VARCHAR(30), job TEXT VARCHAR(20), password TEXT, isAdmin BOOLEAN)""")

c.execute("""INSERT INTO USERS(username, TeamName, email, name, job, password, isAdmin) VALUES("{}", "{}", "{}", "{}", "{}", "{}", {});""".format(username, teamname, email, name, job, hash, True))
con.commit()

#creating Team table =>
c.execute("""CREATE TABLE IF NOT EXISTS TEAMS(id integer primary key AUTOINCREMENT, TeamName TEXT VARCHAR(30), 
          purpose TEXT VARCHAR(300), username TEXT VARCHAR(20),
          job TEXT VARCHAR(30), projectName TEXT VARCHAR(40), TASK TEXT VARCHAR(200), isDone BOOLEAN)""")

c.execute(f"""INSERT INTO TEAMS(TeamName, purpose, username, job) VALUES('{teamname}', '{purpose}', '{username}', '{job}');""")
con.commit()