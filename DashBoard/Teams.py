import streamlit as st
from code_editor import code_editor


def createPage(job, TeamName):
    st.subheader(f":orange[{TeamName}] \n Position : :orange[{job}]", divider = "rainbow")

    Jobs, Information, Apply, Testing  = st.tabs(["Jobs", "Job Description", "Apply", "Testing"])
    # i dont want to take it hard ==! we gonna use samples for just Two teams ==>
    with Jobs:
        with st.form("F1"):
            st.title(":orange[1027]")
            header = st.columns([2,2,1])
            header[0].subheader("Data Scientist")
            header[1].subheader(":red[Full Time]")
            header[2].subheader(":red[Tehran]")
            Teambtn1 = st.form_submit_button('More Info', type="primary", use_container_width=True)

            if Teambtn1:
                st.success("Okay now you can see job information in the Job Description tabs and Apply and do your Test")
                with Information:
                    title = st.columns([2,2,1])
                    title[0].header("Data Scientist", divider="red")
                    title[1].header(":red[Full Time]", divider="red")
                    title[2].header(":red[Tehran]", divider="red")

                    st.write("")
                    st.subheader(":orange[Responsibilities:]", divider="orange")
                    st.write("• Analyze large and complex datasets to extract meaningful insights and trends.")
                    st.write("• Develop and implement machine learning models and algorithms for predictive and prescriptive analytics.")
                    st.write("• Design and execute experiments to test hypotheses and improve models.")
                    st.write("• Collaborate with cross-functional teams to identify business problems and provide data-driven solutions.")

                    st.write(" ")

                    st.subheader(":orange[Requirements:]", divider="orange")
                    st.write("• Proficiency in programming languages such as Python or R, along with libraries like TensorFlow, PyTorch, or scikit-learn.")
                    st.write("• Experience in working with relational databases, SQL, and data querying.")
                    st.write("• Familiarity with cloud platforms like AWS, Azure, or Google Cloud for data storage and processing.")
                    st.write("• Knowledge of data mining techniques and familiarity with tools like Spark or Hadoop.")
                
                with Apply:
                    input1 = st.columns([2,2])
                    first_name = input1[0].text_input("First Name")
                    last_name = input1[1].text_input("Last Name")

                    input2 = st.columns([2,2])
                    Email = input2[0].text_input("Email")
                    PhoneNumber = input2[1].text_input("Phone Number")

                    cover_letter = st.text_area(
                        "Cover Letter",
                    )
                    AI_cover_letter = st.button("Cover Letter Generator", type="primary", use_container_width=True)

                    resume = st.file_uploader("Resume", type="pdf")
                    submit = st.button("Submit", type="primary", use_container_width=True)

        with st.form("F2"):
            st.title(":orange[Sonic]")
            header = st.columns([2,2,1])
            header[0].subheader("Software Engineer")
            header[1].subheader(":red[Full Time]")
            header[2].subheader(":red[Tehran]")
            Teambtn2 = st.form_submit_button('More Info', type="primary", use_container_width=True)

            if Teambtn2:
                st.success("Okay now you can see job information in the Job Description tabs and Apply and do your Test")
                with Information:
                    title = st.columns([2,1,1])
                    title[0].header("Software Engineer", divider="red")
                    title[1].header(":red[Full Time]", divider="red")
                    title[2].header(":red[Tehran]", divider="red")

                    st.write("")
                    st.subheader(":orange[Responsibilities:]", divider="orange")
                    st.write("• Design, develop, and maintain software applications according to business needs and technical specifications..")
                    st.write("• Collaborate with product managers, designers, and other stakeholders to define project requirements and scope.")
                    st.write("• Continuously research and implement best practices, tools, and technologies in software development.")
                    st.write("• Stay up-to-date with industry trends and advancements in software engineering.")

                    st.write(" ")

                    st.subheader(":orange[Requirements:]", divider="orange")
                    st.write("• Strong proficiency in one or more programming languages such as Java, C#, Php, Python, or JavaScript.")
                    st.write("• Solid understanding of software development principles, algorithms, data structures, and design patterns.")
                    st.write("• Familiarity with software development tools and practices such as version control (e.g., Git).")
                    st.write("• Experience with Backend development frameworks (e.g., Spring Boot, Django, Symfony, laravel …).")
                
                with Apply:
                    input1 = st.columns([2,2])
                    first_name = input1[0].text_input("First Name")
                    last_name = input1[1].text_input("Last Name")

                    input2 = st.columns([2,2])
                    Email = input2[0].text_input("Email")
                    PhoneNumber = input2[1].text_input("Phone Number")

                    cover_letter = st.text_area(
                        "Cover Letter",
                    )
                    AI_cover_letter = st.button("Cover Letter Generator", type="primary", use_container_width=True)

                    resume = st.file_uploader("Resume", type="pdf")
                    submit = st.button("Submit", type="primary", use_container_width=True)