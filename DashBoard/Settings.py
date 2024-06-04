import os
import streamlit as st
import pandas as pd
import sqlite3 as sql
import base64

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
    userTab , adminTab, offers = st.tabs(["User Setup", "More", "Offers"])

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
                #JOB TITLE =>
                (f"{job}", "Digital Marketing Specialist", "Web Developer", "Operations Manager", "Network Engineer",
                    "Software Tester", "UX/UI Designer", "Network Administrator", "Software Engineer", "Network Security Specialist",
                     "UI Developer", "Data Analyst", "Systems Administrator", "Database Administrator", "IT Support Specialist",
                      "Project Manager", "Data Engineer", "Database Developer", "Java Developer", "Front-End Engineer", "Back-End Developer",
                       "IT Manager", "Front-End Developer", "Web Designer", "SEM Specialist", "SEO Specialist", "Data Scientist", "SEO Analyst",
                        "Graphic Designer", "IT Administrator")
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

    if job != "admin":
        with offers:
            Information = c.execute(f"""SELECT FirstName, LastName, PhoneNumber, TeamName, Email, Accepted From OFFERS WHERE username = '{username}';""").fetchall()
            column_names = [description[0] for description in c.description]
            data = []
            for row in Information:
                data.append(dict(zip(column_names, row)))

            st.table(data)
    
    elif job == "admin":
        def create_form(username, CoverLetter, n, m):
            with st.form(f"F{n}"):
                header = st.columns([2,2])
                header[0].subheader(f"{username}")
                Accept = header[1].form_submit_button('Accept', type="primary", use_container_width=True)

                if Accept:
                    c.execute(f"""UPDATE OFFERS SET Accepted = {True} WHERE username = "{username}";""")
                    conn.commit()

            with open(f"resume{n}.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()

            Downloads = st.columns([2,2])
            Downloads[0].download_button("Cover Letter", CoverLetter, type="primary", file_name="CoverLetter.txt", use_container_width=True, key={n})
            Downloads[1].download_button("Resume", data=PDFbyte, file_name="resume.pdf", type="primary" ,use_container_width=True, key={m})
            st.subheader("", divider="green")
            
        with offers:
            CoverLetter = c.execute(f"""SELECT username, CoverLetter FROM OFFERS WHERE TeamName = '{TeamName}';""").fetchall()
            n = 0
            m = 100
            for row in CoverLetter:
                n += 1
                m -= 1
                Resume = c.execute(f"""SELECT Resume FROM OFFERS WHERE TeamName = '{TeamName}' AND username = '{row[0]}';""").fetchone()

                print(Resume[0])

                blob = base64.b64decode(Resume[0])
                text_file = open(f"resume{n}.pdf",'wb')
                text_file.write(blob)
                text_file.close()

                create_form(row[0], row[1], n, m)