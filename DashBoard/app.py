import streamlit as st
from streamlit_option_menu import option_menu
from . import Home

def createPage(name):
    #DashBoard sidebar =>
    with st.sidebar:
        st.header(f":orange[{name}]", divider = "rainbow")
        selected = option_menu("DashBoard", ['Home', 'Tasks', 'Assistant', 'Settings'], 
            icons=['house', 'list-task', 'robot', 'gear'], default_index=1,
                styles={
        "container": {"padding": "0!important", "background-color": "lightgray", "border-radius" : "10px"},
        "icon": {"color": "white", "font-size": "20px"}, 
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"5px", "--hover-color": "#eee", "border-radius" : "10px"},
        "nav-link-selected": {"background-color": "orange"},
        }
    )
    
    if selected == "Home":
        Home.createPage()