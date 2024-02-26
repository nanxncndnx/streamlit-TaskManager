import os
import sqlite3 as sql
import streamlit as st
import pandas as pd

def AdminTasks(username):
    #name of the Team =>
    st.title("Dopamine")

    def createProject():
        #data frame of the project =>
        df = pd.DataFrame(
            [
                {"username" : "Null", "job" : "Null", "email" : "Null", "tasks" : "7/10", "status" : 70, "completed" : True},
            ]
        )

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

    #select box for choosing projects =>
    projects = st.selectbox(
        "please choose your project",
        ("classification", "onlineshop"),
        index=None,
        placeholder="select project method ..."
    )

    if projects == "classification":
        loadingProject(projects)

def UserTasks():
    st.subheader("Hello from user")