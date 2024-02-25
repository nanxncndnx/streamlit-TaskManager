import streamlit as st

def createPage():
    st.title("TM assistant")

    with st.sidebar:
        #uploading file and data processing
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            st.write(bytes_data)

    #chat2pdf =>
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})       
        with st.chat_message("user"):
            st.markdown(prompt)
    with st.chat_message("assistant"):
        response = st.write("Hello Human")
    st.session_state.messages.append({"role": "assistant", "content": response})