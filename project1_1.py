# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 08:27:14 2026

@author: PAUL KARIUKI
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time
import os

# Time and date formatting
time_now_p = datetime.now().strftime("%H%M%S")
date_now_p = datetime.now().strftime("%Y%m%d")
time_now = datetime.now().strftime("%H:%M:%S")
date_now = datetime.now().strftime("%Y/%m/%d")

pfile_path = r"C:\Users\USER\Data science databases, excel files and other related statistical tables\Excel Files\students_data_collection.csv"
qfile_folder = r"C:\Users\USER\Coding & Programming Files\Python programming Language Path\My_Streamlit_Apps\project1_1_Q_uploads_files"
qtext_folder = r"C:\Users\USER\Coding & Programming Files\Python programming Language Path\My_Streamlit_Apps\project1_1_Q_uploads_texts"
st.set_page_config(page_title="Students Data Portal", layout="wide")


def load_data():
    if os.path.exists(pfile_path):
        return pd.read_csv(pfile_path)
    else:
        return pd.DataFrame(columns=[
            "First Name", "Last Name", "Age", "Gender", "Grade",
            "Fav_subject", "Disability", "P_Pictures",
            "Submission_time", "Submission_date"
    ])


def save_data(df):
    df.to_csv(pfile_path, index=False)
    
def save_uploaded_question_file(uploaded_qfile):
    """Saves an uploaded file."""
    if not os.path.exists(qfile_folder):
        os.makedirs(qfile_folder)
    
    file_extension = os.path.splitext(uploaded_qfile.name)[1]
    file_count=len(os.listdir(qfile_folder)) + 1
    new_name = f"Q-File{file_count}_{time_now_p}{date_now_p}{file_extension}"
    file_path = os.path.join(qfile_folder, new_name)
    with open(file_path, "wb") as f:
        f.write(uploaded_qfile.getbuffer())
    st.success(f"File saved successfully as: {file_path}")
        
def save_uploaded_question_text(question_text):
    """Saves a text question to a .txt file."""
    if not os.path.exists(qtext_folder):
        os.makedirs(qtext_folder)
        
    file_count = len(os.listdir(qtext_folder)) + 1
    file_path = os.path.join(qtext_folder, f"Question_{file_count}.txt")
    
    with open(file_path, "w") as f:
        f.write(question_text)
    st.success(f"Text question saved successfully as: {file_path}")


st.title(":rainbow[**STUDENTS INFORMATION SYSTE**]")
st.sidebar.button(":blue[_Add a new student_]")

with st.sidebar.form(":red[_Student Form_]", border=True):
    first_name = st.text_input("**First Name**").capitalize()
    last_name = st.text_input("**Last Name**").capitalize()
    age = st.number_input("**Age**", min_value=5, max_value=30, step=1)
    gender = st.selectbox("**Gender**", ["Male", "Female"])
    grade = st.selectbox("**Grade**", ["9th", "10th", "11th", "12th"])
    subject = st.selectbox(
        "**Favourite Subject**",
        ["Mathematics", "Sciences", "Arts", "Religious", "History", "Games & Sports"]
    )
    disability = st.selectbox("**Living with disability**", ["Yes", "No"])

    upload_folder = r"C:\Users\USER\Coding & Programming Files\Python programming Language Path\My_Streamlit_Apps\project1_1_uploaded_images"
    os.makedirs(upload_folder, exist_ok=True)

    profile_pic = st.file_uploader(
        "Upload your profile picture",
        type=["png", "jpg", "jpeg"]
    )
    st.progress(value=0)

    if profile_pic is not None and first_name and last_name:
        file_extension = os.path.splitext(profile_pic.name)[1]
        new_name = f"{first_name}_{last_name}_{time_now_p}{date_now_p}{file_extension}"
        p_file_path = os.path.join(upload_folder, new_name)
        with open(p_file_path, "wb") as f:
            f.write(profile_pic.getbuffer())
        st.success(f"Profile picture saved as: {new_name}")

    submit_button = st.form_submit_button("Save and Submit")

    if submit_button:
        if first_name and last_name:
            try:
                new_row = {
                    "Submission_time": time_now,
                    "Submission_date": date_now,
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Age": age,
                    "Gender": gender,
                    "Grade": grade,
                    "Fav_subject": subject,
                    "Disability": disability,
                    "P_Pictures": new_name
                }
    
                df = load_data()
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
                st.sidebar.success("Data saved and submitted successfully")
            except NameError:
                st.exception(NameError("The uploded file is not supported as a profile picture."))
                st.info("Please upload a supported file type to proceed.")
        else:
            st.warning("Ensure all field are filled or marked complete.")


df = load_data()

if not df.empty:
    tabA, tabB, tabC = st.tabs(["User Info DataFrame",
                                "Visualizations",
                                "User Info Summary"])

    col7, col8, col9 = st.columns(3)
    col10, col11, col12, col13 = st.columns(4)
    
    with tabA:
        st.subheader(":red[Students Registration Data-source]")
        st.dataframe(df, use_container_width=True)
        st.markdown("""
                    <hr style="height:5px;border:2px solid yellow;border-radius:3px;color:powderblue;background-color:#3366ff;" />
                    """, unsafe_allow_html=True)
    
        

    with tabB:
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)
        with col1:
            st.write("**_Students by Subject_**")
            subject_counts = df["Fav_subject"].value_counts()
            fig, ax = plt.subplots()
            ax.bar(subject_counts.index, subject_counts.values,
                   color="purple", edgecolor="turquoise")
            ax.tick_params(axis='x', rotation=45, color='blue')
            ax.minorticks_on()
            ax.grid(True, which="minor", color="gray", linewidth=0.5, alpha=0.5)
            ax.grid(True, which="major", color="darkgray", linewidth=0.8, alpha=0.8)
            ax.set_title("Count of Students Based on Subject")
            ax.set_ylabel("Number of students")
            ax.set_facecolor('palegreen')
            fig.patch.set_facecolor('darkorange')
            st.pyplot(fig, use_container_width=True)

    
        with col2:
            st.write("_**Age Distibution**_")
            fig, ax = plt.subplots()
            bins = list(np.arange(2.5, 33, 2.5))
            ax.hist(df["Age"], bins=bins, color="darkblue",
                    edgecolor="gold", alpha=0.7)
            ax.set_xticks(np.arange(2.5, 33, 2.5))
            ax.tick_params(axis='x', rotation=70, color='red')
            ax.minorticks_on()
            ax.grid(True, which="minor", color="gray", linewidth=0.5, alpha=0.5)
            ax.grid(True, which="major", color="darkgray", linewidth=0.8, alpha=0.8)
            ax.set_title("Age Distribution Among Students")
            ax.set_xlabel("Age")
            ax.set_ylabel("Frequency")
            ax.set_facecolor('pink')
            fig.patch.set_facecolor('darkcyan')
            st.pyplot(fig, use_container_width=True)
            
    
        with col3:
            st.write("_**Number of Males and Females**_")
            gender_counts = df["Gender"].value_counts()
            fig, ax = plt.subplots()
            ax.bar(gender_counts.index, gender_counts.values,
                   color="gold", edgecolor="black")
            ax.minorticks_on()
            ax.grid(True, which="minor", color="gray", linewidth=0.5, alpha=0.5)
            ax.grid(True, which="major", color="darkgray", linewidth=0.8, alpha=0.8)
            ax.set_title("Comparison of number Males & Females")
            ax.set_ylabel("Number of Students")
            ax.set_facecolor('lightblue')
            fig.patch.set_facecolor('darkviolet')
            st.pyplot(fig, use_container_width=True)
        st.markdown("""
                        <hr style="height:5px;border:2px solid red;border-radius:3px;color:#3366ff;background-color:#3366ff;" />
                        """, unsafe_allow_html=True)
            
        with col4:
            st.write(":green[_**Disabilities**_]")
            
            disability_counts = df["Disability"].value_counts()
            fig, ax = plt.subplots()
            ax.bar(disability_counts.index, disability_counts.values, 
                       color='red', edgecolor='black')
            ax.minorticks_on()
            ax.grid(True, which='minor', color='lightgray', linewidth=0.5, alpha=0.5)
            ax.grid(True, which='major', color='gray', linewidth=0.8, alpha=0.8)
            ax.set_title("Disabilities Among Males & Females")
            ax.set_ylabel("Number of Students")
            ax.set_facecolor('gold')
            fig.patch.set_facecolor('limegreen')
            st.pyplot(fig, use_container_width=True)
            
            
        with col5:
            st.write(":green[_**Students at Different Grades**_]")
            
            grade_counts = df["Grade"].value_counts()
            fig, ax = plt.subplots()
            ax.bar(grade_counts.index, grade_counts.values, 
                       color='brown', edgecolor='magenta')
            ax.minorticks_on()
            ax.grid(True, which='minor', color='lightgray', linewidth=0.5, alpha=0.5)
            ax.grid(True, which='major', color='gray', linewidth=0.8, alpha=0.8)
            ax.set_title("Students Against Their Respective Grades")
            ax.set_ylabel("Number of Students")
            ax.set_facecolor('khaki')
            fig.patch.set_facecolor('turquoise')
            st.pyplot(fig, use_container_width=True)
           
        
    
    
    
    with tabC:
        subject_counts = df["Fav_subject"].value_counts()#Count students per subject
        gender_counts = df["Gender"].value_counts()
        
        max_count = subject_counts.max()
        min_count = subject_counts.min()
       
        subjects_with_max = subject_counts[subject_counts == max_count]
        subjects_with_min = subject_counts[subject_counts == min_count]
       
        average_age = df["Age"].mean()
        max_age = df["Age"].max()
        min_age = df["Age"].min()
       
        students_max_age = df[df["Age"] == max_age]
        students_with_max_age = (students_max_age["First Name"] + " " + students_max_age["Last Name"]).tolist()
        students_min_age = df[df["Age"] == min_age]
        students_with_min_age = (students_min_age["First Name"] + " " + students_min_age["Last Name"]).tolist()
        col7, col8, col9, col10 = st.columns(4)
        col11, col12, col13, col14 = st.columns(4)
        with col7:
            st.write(":green[**Data Preview (First 5 rows):**] ")
            st.write(df.head())
            st.write(":green[**Data Preview (Last 5 rows):**] ")
            st.write(df.tail())
            
            
        with col8:
            st.write(":orange[**Columns in DataFrame:**]", df.columns.tolist())\
         
        with col9:    
            st.write(":orange[**Subjects & Gender Counts:**]")
            st.write(subject_counts)
            st.write(gender_counts)
            
        with col10:
            st.write(":orange[**Subjects With Maximum Students:**]")
            for n, (subject, count) in enumerate(subjects_with_max.items(), start=1):
                st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                         f"{n}: **:blue[{subject}]** _with_ **:green[{count}]** _students._")
            st.write(":orange[**Subjects With Minimum Students:**] ")
            for n, (subject, count) in enumerate(subjects_with_min.items(), start=1):
                st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                            f"{n}: **:blue[{subject}]** _with_ **:green[{count}]** _students._")
            st.write(":orange[Minimum Age:] ", min_age)
            st.write(":orange[Students With Minimum Age:] ", students_with_min_age)
            
        with col11:
            st.write(":orange[Average Age:] ",average_age)
            st.write(":orange[Minimum Age:] ", min_age)
            st.write(":orange[Maximum Age:] ", max_age)
            st.write(":orange[Students With Maximum Age:] ", students_with_max_age)
           
            
        with col12:
            st.write(":orange[Students With Minimum Age:] ", students_with_min_age)
           
        
            
        with col13:
            st.write(":yellow[**Students per Grade**]")
            grade_counts = df["Grade"].value_counts()
            st.write(grade_counts)
            st.write(":orange[**Disability Status Among Students**]")
            dis_counts = df["Disability"].value_counts()
            st.write(dis_counts)
        
        st.divider()
        
             
else:
    st.info("No data available. Use the sidebar to add data.")


tab1, tab2 = st.tabs(["Text Input", "File Upload"])

with tab1:
    st.subheader(":rainbow[**Submit via Text**]")
    question_text = (st.text_area(":blue[_Type your question here:_]")).strip().capitalize()
    if st.button(":orange[Save Text Question]"):
        if question_text:
            with st.spinner(":green[_Saving your question..._]"):
                time.sleep(1)
                save_uploaded_question_text(question_text)
            st.success("Thankyou so much for your feedback. \nWe are glad you are enjoying the experience with our app.")
                
        else:
            st.warning("The space is empty! Please enter a question to submit.")
            
with tab2:
    st.subheader(":rainbow[**Submit via File Upload**]")
    uploaded_qfile = st.file_uploader(":blue[_Choose a file:_]", type=None)#Allow all file types
    if st.button(":orange[Save Uploaded File]"):
        if uploaded_qfile is not None:
            with st.spinner(f":green[Uploading {uploaded_qfile.name}...]"):
                time.sleep(8)
                save_uploaded_question_file(uploaded_qfile)
            st.success("Thankyou so much for your feedback. \nWe are glad you are enjoying the experience with our app. ")
        else:
            st.warning("File not uploaded! Please upload a file to submit.")














