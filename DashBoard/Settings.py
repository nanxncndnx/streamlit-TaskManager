import os
import streamlit as st
import sqlite3 as sql
from dotenv import load_dotenv

def createPage(name, username, email, job, TeamName):
    st.subheader("Account Setup")

    #loadin data from .env and connecting database =>
    load_dotenv()
    BASE_DIR = os.getenv("DB_path")
    db_user = os.path.join(BASE_DIR, "User.db")
    conn = sql.connect(db_user)
    c = conn.cursor()

    #creating tabs for Admin setup and user setup =>
    userTab , adminTab = st.tabs(["User Setup", "Admin Setup"])

    with userTab:
        col1, col2 = st.columns(2)

        with col1:
            Uname = st.text_input("username", value=username, disabled=True)
            firstName = st.text_input("name", value=name, disabled=True)
            Uemail = st.text_input("email", value=email, disabled=True)

        with col2:
            UTeam = st.text_input("Team Name", value=TeamName)
            Ujob = st.selectbox(
                "Job and your position",
                (f"{job}", "Two", "Three")
            )

        btn = st.button("update", type="primary", use_container_width=True)
        if btn and UTeam:
            #checking Team exists in table =>
            try:
                c.execute(f"""SELECT username FROM USERS WHERE TeamName = '{UTeam}';""")
                #updating job and team name in USERS table =>
                c.execute(f"""UPDATE USERS SET TeamName = '{UTeam}' , job = '{Ujob}' , isAdmin = {False} WHERE username = '{username}';""")
                conn.commit()
                st.success("Your account updated successfully")
            except:
                st.error("This Team Name not exists")

        elif btn:
            st.error("Please fill inputs")
    
    with adminTab:
        #if member do not have team then he/she can create team =>
        if job == None and TeamName == None:
            name_Team = st.text_input("Team Name")
            purpose = st.text_input("your purpose")
            Teambtn = st.button("create Team" , type="primary", use_container_width=True)

            if Teambtn and name_Team and purpose:
                try:
                    #checking Team Name is availble or not =>
                    c.execute(f"""SELECT username FROM TEAMS WHERE TeamName = '{name_Team}';""")

                    #inserting team info to TEAMS table =>
                    c.execute(f"""INSERT INTO TEAMS(TeamName, purpose, username, job) VALUES('{name_Team}', '{purpose}', '{username}', 'admin');""")
                    conn.commit()

                    #updating team name and job in USERS table =>
                    c.execute(f"""UPDATE USERS SET TeamName = '{name_Team}' , job = 'admin' , isAdmin = {True} WHERE username = '{username}';""")
                    conn.commit()

                    #create dir for csv files about team projects =>
                    dir = name_Team
                    parent_dir = "/home/nanxncndnx/Documents/MachineLearning/TM/streamlit-TaskManager/DashBoard/csv_data"
                    path = os.path.join(parent_dir , dir)
                    os.mkdir(path)

                    st.success("Team created successfully")

                except:
                    st.error("this Team Name already taken!")

            elif Teambtn:
                st.error("Please fill inputs")

        #also if member have team and job he/she can not create team
        elif job != "admin" and job != None and TeamName != None:
            st.error(f"Well you are {job} in {TeamName} you can not create team")
        
        elif job == "admin":
            st.subheader("Hello boss")