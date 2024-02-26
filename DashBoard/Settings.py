import streamlit as st

def createPage(name, username, email):
    st.subheader("Account Setup")

    col1, col2 = st.columns(2)

    with col1:
        Uname = st.text_input("username", value=username, disabled=True)
        firstName = st.text_input("name", value=name, disabled=True)
        Uemail = st.text_input("email", value=email, disabled=True)

    with col2:
        TeamName = st.text_input("Team Name", placeholder="please enter name of the team")
        job = st.selectbox(
            "Job and your position",
            ("one", "Two")
        )

    btn = st.button("update", type="primary", use_container_width=True)