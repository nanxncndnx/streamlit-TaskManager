import os
import os.path
import sys
import sqlite3 as sql
import streamlit as st
import pandas as pd

from dotenv import load_dotenv
from . import Model

def AdminTasks(username, job, TeamName, email):
    #name of the Team =>
    st.subheader(f":orange[{TeamName}] \nPosition : :orange[{job}]", divider = "rainbow")

    #loadin data from .env and connecting database =>
    load_dotenv()
    BASE_DIR = os.getenv("DB_path")
    CSV_DIR = os.getenv("csv_path")
    db_user = os.path.join(BASE_DIR, "User.db")
    conn = sql.connect(db_user)
    c = conn.cursor()

    def createProject(username, job, email, TeamName, ProjectName, ProjectInfo):
        #data frame of the project =>
        df = pd.DataFrame(
            [
                {"username" : username, "job" : job, "email" : email, "tasks" : ProjectInfo, "status" : 0, "completed" : False},
            ]
        )

        #saving dataframe as csv file in team dir =>
        df.to_csv(f"{CSV_DIR}/{TeamName}/{ProjectName}.csv")
        st.success("Project created successfully")

    #lets add the new member to csv file of the project in team dir =>
    def new_member_csvProject(username, job, email, TeamName, CSV_DIR, projectName):
        df = pd.read_csv(f"{CSV_DIR}/{TeamName}/{projectName}.csv")
        new_member = {"username" : username, "job" : job, "email" : email, "tasks" : f"{0}/{1}", "status" : 0, "completed" : False}
        df.loc[len(df)] = new_member
        df.to_csv(f"{CSV_DIR}/{TeamName}/{projectName}.csv")
        st.success("Task added successfully")

    #loading Team projects as data editor =>
    def loadingProject(projects):
        st.subheader(projects)

        #connecting to the csv file of the project =>
        df = pd.read_csv(f"{CSV_DIR}/{TeamName}/{projects}.csv")

        #extracting username of the all members in team=>
        All_members = c.execute(f"""SELECT DISTINCT username FROM TEAMS WHERE projectName = "{projects}"; """).fetchall()
        
        #updating member tasks in csv project file from sql=>
        for name in All_members:
            counting_tasks_user = len(c.execute(f"""SELECT * FROM TEAMS WHERE projectName = "{projects}" AND username = "{name[0]}"; """).fetchall())
            counting_isDone_user = len(c.execute(f"""SELECT * FROM TEAMS WHERE projectName = "{projects}" AND isDone = {True} AND username = "{name[0]}" ; """).fetchall())
            
            #now we gonna update Task memebers and status memebers
            updated_user = df["username"] == name[0]
            df.loc[updated_user, "tasks"] = f"{counting_isDone_user}/{counting_tasks_user}"

            #calculating status =>
            percent = counting_isDone_user / counting_tasks_user * 100
            df.loc[updated_user, "status"] = percent
            df.to_csv(f"{CSV_DIR}/{TeamName}/{projects}.csv")

        #updating total tasks in csv project file from sql=>
        counting_tasks = len(c.execute(f"""SELECT * FROM TEAMS WHERE projectName = "{projects}"; """).fetchall())
        counting_isDone = len(c.execute(f"""SELECT * FROM TEAMS WHERE projectName = "{projects}" AND isDone = {True}; """).fetchall())

        updated_total = df["username"] == username
        df.loc[updated_total, "tasks"] = f"{counting_isDone}/{counting_tasks}"

        #calculating status =>
        percent = counting_isDone / counting_tasks * 100
        df.loc[updated_total, "status"] = percent
        df.to_csv(f"{CSV_DIR}/{TeamName}/{projects}.csv")

        #column data of the project =>
        st.data_editor(df[["username", "job", "email", "tasks", "status", "completed"]])

    #creating tabs for loading and creating projects =>
    CreateProjectTab, AddingTask, StatusTab = st.tabs(["Create Project", "Adding Task", "Status"])

    with StatusTab:
        #find all projects created by this team =>
        projects_dir = f"{CSV_DIR}/{TeamName}"
        files = [f.split('.')[0] for f in os.listdir(projects_dir)]
        files = tuple(files)

        #select box for choosing projects =>
        projects = st.selectbox(
            "please choose your project",
            files,
            index=None,
            placeholder="select project method ..."
        )

        if projects != None:
            loadingProject(projects)

    #create text input for project name =>
    with CreateProjectTab:
        ProjectName = st.text_input("Enter The Project Name", placeholder = "HAVE TO BE UNIQE")
        ProjectInfo = st.text_input("Please explain about the project" , placeholder = "What is your goals for this project and ...")
        btnProject = st.button("Create", type="primary", use_container_width=True)

        #checking project name is uniqe and ... =>
        if btnProject and ProjectName and ProjectInfo:
            if os.path.exists(f"{ProjectName}.csv"):
                st.error(f"{ProjectName} project is already exists in {TeamName} team projects")
            else:
                createProject(username, job, email, TeamName, ProjectName, ProjectInfo)

    #Adding Tasks to the Projects by Admin =>
    with AddingTask:
        #find all projects created by this team =>
        projects_dir = f"{CSV_DIR}/{TeamName}"
        files = [f.split('.')[0] for f in os.listdir(projects_dir)]

        #inputs and multi selectbox ... =>
        allProjects = st.multiselect(
            "please select projects",
            files,
        )

        TaskInfo = st.text_input("Please Explain The Task", placeholder = "create login form with ...")
        btnTask = st.button("Add", type="primary", use_container_width=True)

        #checking button and text input =>
        if TaskInfo and btnTask:
            with st.spinner('Wait for it...'):
                #classification job ...
                answer = Model.classification(TaskInfo)
                st.write(answer)

            #lets found who can do the task in this team =>
            try:
                personUsername, personEmail = c.execute(f"""SELECT username, email FROM USERS WHERE job = "{answer}" AND TeamName = "{TeamName}"; """).fetchone()
            except:
                st.error(f"No one can do this task in your team you need a {answer}")
                st.stop()

            #now we can update the teams table =>
            for i in allProjects:
                #we dont want same tasks in each project then we should controll them =>
                #please fix this part this take so much time finde better solution !!!!!
                if c.execute(f""" SELECT * FROM TEAMS WHERE username = "{personUsername}" AND projectName = "{i}" AND TASK = "{TaskInfo}"; """).fetchone() != None:
                    st.error("we have same task in this project!")
                else:
                    c.execute(f"""INSERT INTO TEAMS (TeamName, username, job, projectName, Task, isDone) VALUES("{TeamName}", "{personUsername}",
                            "{answer}", "{i}", "{TaskInfo}", {False});""")
                    conn.commit()

                    #lets connect to the csv file and check the member is in the project or not ! =>
                    df_project = pd.read_csv(f"{CSV_DIR}/{TeamName}/{i}.csv")
                    if df_project.isin([personUsername]).any().any():
                        #updating task and status cell from csv file =>
                        counting_tasks = len(c.execute(f"""SELECT * FROM TEAMS WHERE username = "{personUsername}" AND projectName = "{i}"; """).fetchall())
                        counting_isDone = len(c.execute(f"""SELECT * FROM TEAMS WHERE username = "{personUsername}" AND projectName = "{i}" AND isDone = {True}; """).fetchall())

                        updated = df_project["username"] == personUsername
                        df_project.loc[updated, "tasks"] = f"{counting_isDone}/{counting_tasks}"

                        #calculating status =>
                        percent = counting_isDone / counting_tasks * 100
                        df_project.loc[updated, "status"] = percent
                        df_project.to_csv(f"{CSV_DIR}/{TeamName}/{i}.csv")
                        st.success("Task added Successfully")
                    else:
                        new_member_csvProject(personUsername, answer, personEmail, TeamName, CSV_DIR, i)

def UserTasks(username, job, TeamName):
    st.subheader(f":orange[{TeamName}] \nPosition : :orange[{job}]", divider = "rainbow")

    #loadin data from .env and connecting database =>
    load_dotenv()
    BASE_DIR = os.getenv("DB_path")
    CSV_DIR = os.getenv("csv_path")
    db_user = os.path.join(BASE_DIR, "User.db")
    conn = sql.connect(db_user)
    c = conn.cursor()

    try:
        df = pd.read_sql(f"""SELECT projectName, TASK, isDone FROM TEAMS WHERE username = "{username}"; """, conn)
        edited_df = st.data_editor(df)

        isDone = edited_df["isDone"]
        projectName = edited_df["projectName"]
        Task = edited_df["TASK"]

        if isDone[0] == 0:
            c.execute(f"""UPDATE TEAMS SET isDone = {False} WHERE username = "{username}" AND projectName = "{projectName[0]}" AND TASK = "{Task[0]}";""")
            conn.commit()
            st.success("status changed successfuly to False")
        elif isDone[0] == 1:
            c.execute(f"""UPDATE TEAMS SET isDone = {True} WHERE username = "{username}" AND projectName = "{projectName[0]}" AND TASK = "{Task[0]}";""")
            conn.commit()
            st.success("status changed successfuly to True")
    except:
        pass