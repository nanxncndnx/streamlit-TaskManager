import os
import sqlite3 as sql
from dotenv import load_dotenv
import streamlit as st
from streamlit_option_menu import option_menu
from . import Home, Teams, Tasks, Settings

def createPage(name , username):
    #loadin data from .env and connecting database =>
    load_dotenv()
    BASE_DIR = os.getenv("DB_path")
    db_user = os.path.join(BASE_DIR, "User.db")
    conn = sql.connect(db_user)
    c = conn.cursor()

    #extract the email address =>
    email = c.execute(f"""SELECT email, password FROM USERS WHERE username = '{username}'; """).fetchone()
    job_TeamName = c.execute(f"""SELECT job , TeamName FROM USERS WHERE username = '{username}';""").fetchone()

    #DashBoard sidebar =>
    with st.sidebar:
        #check the job and TeameName =>
        if  job_TeamName == (None, None):
            st.warning("Please complete your account setup from settings and find your team from Teams")

        st.header(f"Welcome :orange[{name}]", divider = "rainbow")
        selected = option_menu("DashBoard", ['Home', 'Tasks', 'Teams', 'Settings'], 
            icons=['house', 'list-task', 'microsoft-teams', 'gear'], default_index=1,
                styles={
        "container": {"padding": "important", "background-color": "#0F161E", "border-radius" : "10px"},
        "icon": {"color": "white", "font-size": "20px"}, 
        "nav-link": {"font-size": "20px", "text-align": "center", "margin":"10px", "--hover-color": "#eee", "border-radius" : "10px"},
        "nav-link-selected": {"background-color": "orange"},
        }
    )

    #check admin =>
    check_admin = False
    isAdmin = c.execute(f"""SELECT isAdmin FROM USERS WHERE username = '{username}' ;""")
    isAdmin = isAdmin.fetchone()

    if isAdmin[0] == 1:
        check_admin = True
    
    #pages =>
    if selected == "Home":
        Home.createPage()

    if selected == "Tasks" and check_admin == True:
        Tasks.AdminTasks(username, job_TeamName[0], job_TeamName[1], email[0])
    elif selected == "Tasks" and check_admin == False:
        Tasks.UserTasks(username, job_TeamName[0], job_TeamName[1])

    if selected == "Teams":
        Teams.createPage(username, job_TeamName[0], job_TeamName[1])

    if selected == "Settings":
        Settings.createPage(name, username, email[0], job_TeamName[0], job_TeamName[1])