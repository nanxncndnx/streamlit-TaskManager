import os.path 
import time
import sqlite3 as sql
import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import altair as alt
from dotenv import load_dotenv

from DashBoard import app

load_dotenv()
alt.themes.enable("dark")

#open yaml file =>
with open('./data/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

#loadin and connecting database =>
BASE_DIR = os.getenv("DB_path")
db_user = os.path.join(BASE_DIR, "User.db")
conn = sql.connect(db_user)
c = conn.cursor()

def yaml2db(username, user_info, conn, c):
    #extract info from Dict value =>
    email, name, password = user_info["email"], user_info["name"], user_info["password"]
    c.execute(f"""INSERT INTO USERS(username, email, name, password) VALUES('{username}', '{email}', '{name}', '{password}');""")
    conn.commit()

#authenticate confiuration =>
def authentication_yaml(user_info):
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    return authenticator

#SQLite database into dictionaries =>
def sql_to_dict(conn, c):
    #function for get columns and values = > 
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    conn.row_factory = dict_factory
    c = conn.cursor()

    Dict1 = { }
    Dict2 = { }
    res = c.execute(""" SELECT * FROM USERS """)
    res = res.fetchone()
    username = res["username"]
    Dict1[username] = res
    Dict2["usernames"] = Dict1

    return Dict2

#Login Form =>
def Login(authenticator):
    authenticator.login()
    if st.session_state["authentication_status"]:
        name = st.session_state["name"]
        username = st.session_state["username"]
        app.createPage(name , username)

    elif st.session_state["authentication_status"] is False:
        st.error('Username or password is incorrect')

    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

#Creating a new user registration =>
def register_user(authenticator, conn, c):
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
        if email_of_registered_user:
            #inser user info to yaml file =>
            with open('./data/config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            st.success('User registered successfully')

            #extract info from yaml format value =>
            username = username_of_registered_user
            for user in config['credentials'].items():
                user_info = user[1][username]

            yaml2db(username , user_info, conn, c)
    except Exception as e:
        st.error(e)

#Login/Register form =>
selected = option_menu(None, ["Register", "Login", "Logout"], 
    icons=['person-fill-add', 'person-fill-check', 'person-fill-dash'], 
    default_index=0, orientation="horizontal",
    styles={
    "container": {"padding": "0!important", "background-color": "#0F161E", "border-radius" : "15px"},
    "icon": {"color": "white", "font-size": "15px"}, 
    "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee", "border-radius" : "20px"},
    "nav-link-selected": {"background-color": "orange"},
    }
)

if selected == "Login":
    user_info = sql_to_dict(conn , c)
    authenticator = authentication_yaml(user_info)
    Login(authenticator)

if selected == "Register":
    user_info = sql_to_dict(conn , c)
    authenticator = authentication_yaml(user_info)
    register_user(authenticator, conn , c)

if selected == "Logout":
    if st.session_state["authentication_status"]:
        user_info = sql_to_dict(conn , c)
        authenticator = authentication_yaml(user_info)
        authenticator.logout()