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

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "show_form" not in st.session_state:
    st.session_state.show_form = False

# -------------------------------------------------
# Time and date formatting
# -------------------------------------------------
time_now_p = datetime.now().strftime("%H%M%S")
date_now_p = datetime.now().strftime("%Y%m%d")
time_now = datetime.now().strftime("%H:%M:%S")
date_now = datetime.now().strftime("%Y/%m/%d")

# -------------------------------------------------
# File paths
# -------------------------------------------------
pfile_path = r"C:\Users\USER\Data science databases, excel files and other related statistical tables\Excel Files\students_data_collection.csv"
qfile_folder = r"C:\Users\USER\Coding & Programming Files\Python programming Language Path\My_Streamlit_Apps\project1_1_Q_uploads_files"
qtext_folder = r"C:\Users\USER\Coding & Programming Files\Python programming Language Path\My_Streamlit_Apps\project1_1_Q_uploads_texts"

st.set_page_config(page_title="Students Data Portal", layout="wide")

# -------------------------------------------------
# Data functions
# -------------------------------------------------
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
    if not os.path.exists(qfile_folder):
        os.makedirs(qfile_folder)
    file_extension = os.path.splitext(uploaded_qfile.name)[1]
    file_count = len(os.listdir(qfile_folder)) + 1
    new_name = f"Q-File{file_count}_{time_now_p}{date_now_p}{file_extension}"
    file_path = os.path.join(qfile_folder, new_name)
    with open(file_path, "wb") as f:
        f.write(uploaded_qfile.getbuffer())
    st.success(f"File saved successfully as: {file_path}")

def save_uploaded_question_text(question_text):
    if not os.path.exists(qtext_folder):
        os.makedirs(qtext_folder)
    file_count = len(os.listdir(qtext_folder)) + 1
    file_path = os.path.join(qtext_folder, f"Question_{file_count}.txt")
    with open(file_path, "w") as f:
        f.write(question_text)
    st.success(f"Text question saved successfully as: {file_path}")

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title(":rainbow[**STUDENTS INFORMATION SYSTEM**]")

# -------------------------------------------------
# Sidebar Form
# -------------------------------------------------
with st.sidebar:
    if st.button(":blue[_Add a new student_]"):
        st.session_state.show_form = True

    if st.session_state.show_form:
        with st.form(key=":rainbow[_Student Form_]"):
            first_name = st.text_input("**First Name**").capitalize()
            last_name = st.text_input("**Last Name**").capitalize()
            age = st.number_input("**Age**", min_value=5, max_value=30, step=1)
            gender = st.selectbox("**Gender**", ["Male", "Female"])
            grade = st.selectbox("**Grade**", ["9th", "10th", "11th", "12th"])
            subject = st.selectbox("**Favourite Subject**",
                ["Mathematics", "Sciences", "Arts", "Religious", "History", "Games & Sports"])
            disability = st.selectbox("**Living with disability**", ["Yes", "No"])

            upload_folder = r"C:\Users\USER\Coding & Programming Files\Python programming Language Path\My_Streamlit_Apps\project1_0_uploaded_images"
            os.makedirs(upload_folder, exist_ok=True)

            profile_pic = st.file_uploader("Upload your profile picture",
                                           type=["png", "jpg", "jpeg"])
            st.progress(0)

            new_name = ""
            if profile_pic is not None and first_name and last_name:
                file_extension = os.path.splitext(profile_pic.name)[1]
                new_name = f"{first_name}_{last_name}_{time_now_p}{date_now_p}{file_extension}"
                p_file_path = os.path.join(upload_folder, new_name)
                with open(p_file_path, "wb") as f:
                    f.write(profile_pic.getbuffer())
                st.success(f"Profile picture saved as: {new_name}")

            submit_button = st.form_submit_button("Save and Submit")
            if submit_button and first_name and last_name:
                df = load_data()
                df = pd.concat([df, pd.DataFrame([{
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
                }])], ignore_index=True)
                save_data(df)
                st.sidebar.success("Data saved and submitted successfully")
                st.session_state.show_form = False

# -------------------------------------------------
# Load Data
# -------------------------------------------------
df = load_data()

if not df.empty:
    tabA, tabB, tabC = st.tabs([
        "User Info DataFrame",
        "Visualizations",
        "User Info Summary"
    ])

    # ---------------- TAB A ----------------
    with tabA:
        st.dataframe(df, use_container_width=True)
        st.write("Rows:", df.shape[0], " | Columns:", df.shape[1])
        st.write("Missing Values Per Column:")
        st.write(df.isnull().sum())

    # ---------------- TAB B ----------------
    with tabB:
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            df["Grade"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
            ax.set_ylabel("")
            ax.set_title("Students per Grade")
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            df["Disability"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
            ax.set_ylabel("")
            ax.set_title("Disability Status Distribution")
            st.pyplot(fig)

        col3, col4 = st.columns(2)

        with col3:
            fig, ax = plt.subplots()
            df.boxplot(column="Age", by="Grade", ax=ax)
            ax.set_title("Age Distribution per Grade")
            ax.set_ylabel("Age")
            st.pyplot(fig)

        with col4:
            cross = pd.crosstab(df["Fav_subject"], df["Gender"])
            fig, ax = plt.subplots()
            cross.plot(kind="bar", ax=ax)
            ax.set_title("Favourite Subject by Gender")
            ax.set_ylabel("Number of Students")
            st.pyplot(fig)

    # ---------------- TAB C ----------------
    with tabC:
        st.write("Total Students:", len(df))

        gender_pct = df["Gender"].value_counts(normalize=True) * 100
        st.write("Gender Percentage (%):")
        st.write(gender_pct.round(2))

        disability_pct = df["Disability"].value_counts(normalize=True) * 100
        st.write("Disability Percentage (%):")
        st.write(disability_pct.round(2))

        st.write("Most Common Grade:", df["Grade"].mode()[0])
        st.write("Most Popular Subject:", df["Fav_subject"].mode()[0])

        oldest = df.loc[df["Age"].idxmax()]
        youngest = df.loc[df["Age"].idxmin()]

        st.write("Oldest Student:", oldest["First Name"], oldest["Last Name"], "-", oldest["Age"])
        st.write("Youngest Student:", youngest["First Name"], youngest["Last Name"], "-", youngest["Age"])

else:
    st.info("No data available. Use the sidebar to add data.")
