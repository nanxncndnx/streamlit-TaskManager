import os
import sqlite3 as sql
import streamlit as st
import pandas as pd

def AdminTasks(username, job, TeamName):
    #name of the Team =>
    st.subheader(f":orange[{TeamName}] \nPosition : :orange[{job}]", divider = "rainbow")

    def createProject(TeamName, ProjectName):
        #data frame of the project =>
        df = pd.DataFrame(
            [
                {"username" : None, "job" : None, "email" : None, "tasks" : None, "status" : None, "completed" : None},
            ]
        )

        #saving dataframe as csv file =>
        df.to_csv(f"/home/nanxncndnx/Documents/MachineLearning/TM/streamlit-TaskManager/DashBoard/csv_data/{TeamName}/{ProjectName}.csv")
        st.success("Project created successfully")

    #loading Team projects as data editor =>
    def loadingProject(projects):
        st.subheader(projects)

        #data frame of the project =>
        df = pd.DataFrame(
            [
                {"username" : "Null", "job" : "Null", "email" : "Null", "tasks" : "7/10", "status" : 70, "completed" : True},
                {"username" : "Null", "job" : "Null", "email" : "Null", "tasks" : "3/10", "status" : 30, "completed" : True},
            ]
        )

        #column data of the project =>
        st.data_editor(
            df,
            column_config={
                "usernames" : st.column_config.TextColumn(
                    "usernames",
                    max_chars=30,
                ),
                "job" : st.column_config.TextColumn( 
                    "job",
                    max_chars=20,
                ),
                "email" : st.column_config.TextColumn(
                    "email",
                    max_chars=30,
                ),
                "tasks" : st.column_config.SelectboxColumn(
                    "tasks",
                ),
                "status" : st.column_config.ProgressColumn(
                    "status",
                    min_value = 0,
                    max_value = 100,
                ),
                "completed" : st.column_config.CheckboxColumn(
                    "completed",
                    default=False,
                )
            },

            disabled=["tasks"],
            hide_index=True,
        )

    #creating tabs for loading and creating projects =>
    CreateProjectTab, AddingTask, StatusTab = st.tabs(["Create Project", "Adding Task", "Status"])

    with StatusTab:
        #select box for choosing projects =>
        projects = st.selectbox(
            "please choose your project",
            ("classification", "onlineshop"),
            index=None,
            placeholder="select project method ..."
        )

        if projects == "classification":
            loadingProject(projects)

    #create text input for project name =>
    with CreateProjectTab:
        ProjectName = st.text_input("Enter The Project Name", placeholder = "HAVE TO BE UNIQE")
        btnProject = st.button("Create", type="primary", use_container_width=True)

        #checking project name is uniqe and ... =>
        if btnProject and ProjectName:
            if os.path.exists(f"{ProjectName}.csv"):
                st.error(f"{ProjectName} project is already exists in {TeamName} team projects")
            else:
                createProject(TeamName, ProjectName)

    #Adding Tasks to the Projects by Admin =>
    with AddingTask:
        st.write("Hello")

def UserTasks(username, job, TeamName):
    st.subheader(f":orange[{TeamName}] \nPosition : :orange[{job}]", divider = "rainbow")