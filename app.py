import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np
import scipy as sp
# STREAMLIT
st.title("Students Performance Factor")


file_path = "students_performance_factor.csv"
with open(file_path, "rb") as f:
    st.download_button(
        label="Download Dataset",
        data=f,
        file_name="students_performance_factor.csv",
        mime="text/csv"
    )
        # LOAD DATA
st.header("Load Dataset")
data = pd.read_csv("students_performance_factor.csv")
       # Show Raw Data
if st.checkbox("show raw data"):
    st.subheader("Raw Data")
    st.dataframe(data)
st.subheader("Basic Info")
st.write(data.info())

st.subheader("Shape")
st.write(data.shape)

st.subheader("Columns")
st.write(data.columns)

st.subheader("Describe")
st.write(data.describe())

st.subheader("Head")
st.write(data.head(10))

st.subheader("Tails")
st.write(data.tail(10))
   
st.subheader("Parental Involvement Counts") 
st.dataframe(data["Parental_Involvement"].value_counts().to_frame()) 

st.subheader("Access to Resources Counts") 
st.dataframe(data["Access_to_Resources"].value_counts().to_frame())

st.subheader("Extracurricular Activities Counts") 
st.dataframe(data["Extracurricular_Activities"].value_counts().to_frame())

stats = data["Hours_Studied"].agg(["count", "min", "mean", "max"]).round().to_frame() 
st.subheader("Hours Studied Summary Statistics") 
st.dataframe(stats)

data["Teacher_Quality"] = data["Teacher_Quality"].fillna(data["Teacher_Quality"].mode()[0]) 
st.subheader("Teacher Quality (after filling missing values)")
st.dataframe(data["Teacher_Quality"].value_counts().to_frame())

st.subheader("Missing Values Summary") 
st.dataframe(data.isnull().sum().to_frame())

duplicates = data.duplicated().sum() 
st.subheader("Duplicate Rows in Dataset") 
st.write(f"Number of duplicate rows: {duplicates}")

grouped_counts = ( data.groupby("Parental_Education_Level")["Family_Income"] .value_counts() .to_frame() ) 
st.subheader("Family Income by Parental Education Level")
st.dataframe(grouped_counts)

grouped_counts = ( data.groupby("School_Type")["Teacher_Quality"] .value_counts() .reset_index(name="count") ) 
st.subheader("Teacher Quality Distribution by School Type")
fig = px.bar( grouped_counts, x="School_Type", y="count", color="Teacher_Quality", barmode="group", title="Teacher Quality Counts by School Type" ) 
st.plotly_chart(fig, use_container_width=True)

grouped_stats = ( data.groupby("Attendance")["Exam_Score"] .agg(["count", "min", "mean", "max"]) .round() .reset_index() ) 
sampled_stats = grouped_stats.sample(5) 
st.subheader("Exam Score Summary by Attendance") 
fig = px.bar( sampled_stats, x="Attendance", y="count", title="Exam Score Counts by Attendance", text="count" ) 
st.plotly_chart(fig, use_container_width=True)

grouped_stats = ( data.groupby("Sleep_Hours")["Exam_Score"] .agg(["count", "min", "mean", "max"]) .round() )
st.subheader("Exam Score Summary by Sleep Hours")
fig, ax = plt.subplots(figsize=(8, 5)) 
grouped_stats.plot(kind="bar", ax=ax) 
ax.set_title("Exam Score Statistics by Sleep Hours") 
ax.set_ylabel("Values") 
ax.set_xlabel("Sleep Hours") 
plt.xticks(rotation=45)
st.pyplot(fig)

data["Distance_from_Home"] = data["Distance_from_Home"].map({"Far":0, "Moderate":1, "Near":2}) 
st.subheader("Distance from Home (Numeric Mapping)")
st.dataframe(data[["Distance_from_Home"]])
fig = px.histogram( data, x="Distance_from_Home", nbins=3, 
                   title="Distribution of Distance from Home", 
                   labels={"Distance_from_Home": "Distance from Home (0=Far, 1=Moderate, 2=Near)"} ) 
st.plotly_chart(fig, use_container_width=True)




