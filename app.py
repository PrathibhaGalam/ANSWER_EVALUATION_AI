import streamlit as st
import pandas as pd
import re

from rag.pdf_loader import load_pdfs
from rag.vector_store import create_vectorstore
from rag.rag_chain import create_rag_chain
from rag.question_splitter import split_questions, split_student_answers
# app.py
from prompts.evaluation_prompt import evaluation_prompt

from dotenv import load_dotenv
load_dotenv()

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="AI Answer Script Evaluation",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM UI STYLE
# -------------------------------------------------

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
background-color:#0f172a;
}

h1{
color:#60a5fa;
text-align:center;
}

.stButton>button{
background: linear-gradient(90deg,#2563eb,#3b82f6);
color:white;
border-radius:10px;
height:3em;
width:220px;
font-size:16px;
}

.stButton>button:hover{
background:#1d4ed8;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("🤖 AI Answer Script Evaluation Assistant")

st.markdown("""
This intelligent system evaluates **student answer scripts automatically**
using **Retrieval Augmented Generation (RAG)** and **Large Language Models**.
""")

st.divider()

# -------------------------------------------------
# EXAM INFORMATION
# -------------------------------------------------

st.subheader("📘 Exam Information")

col1, col2, col3 = st.columns(3)

with col1:

    department = st.selectbox(
        "Select Department",
        [
            "Computer Science Engineering",
            "Artificial Intelligence & Machine Learning",
            "Information Technology",
            "Electronics and Communication Engineering",
            "Mechanical Engineering",
            "Civil Engineering"
        ]
    )

    subject = st.text_input("Enter Subject Name")

with col2:

    subject_code = st.text_input(
        "Enter Subject Code",
        placeholder="Example: 22CS201"
    )

    exam_date = st.date_input("Select Exam Date")

with col3:

    student_year = st.selectbox(
        "Student Year",
        [
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year"
        ]
    )

st.divider()

# -------------------------------------------------
# FILE UPLOAD SECTION
# -------------------------------------------------

st.subheader("📂 Upload Files")

col4, col5 = st.columns(2)

with col4:

    correct_pdf = st.file_uploader(
        "Upload Correct Answer PDF",
        type="pdf"
    )

with col5:

    student_pdfs = st.file_uploader(
        "Upload Student Answer PDFs",
        type="pdf",
        accept_multiple_files=True
    )

# -------------------------------------------------
# EVALUATION BUTTON
# -------------------------------------------------

if st.button("🚀 Evaluate Answers"):

    if not correct_pdf or not student_pdfs:
        st.warning("Please upload both Correct Answer PDF and Student PDFs.")
        st.stop()

    with st.spinner("🤖 AI is evaluating student answers..."):

        # -------------------------------------------------
        # LOAD CORRECT ANSWERS
        # -------------------------------------------------

        correct_chunks = load_pdfs([correct_pdf])

        correct_text = ""

        for chunk in correct_chunks:
            correct_text += chunk["text"] + "\n"

        # Split correct answers Q1–Q6
        correct_questions = split_questions(correct_text)

        correct_texts = [chunk["text"] for chunk in correct_chunks]

        # -------------------------------------------------
        # CREATE VECTOR DATABASE
        # -------------------------------------------------

        collection = create_vectorstore(correct_texts)

        # -------------------------------------------------
        # CREATE RAG CHAIN
        # -------------------------------------------------

        rag_chain = create_rag_chain(collection)

        # -------------------------------------------------
        # LOAD STUDENT ANSWERS
        # -------------------------------------------------

        students = load_pdfs(student_pdfs)

        results_table = []

        st.subheader("📑 Individual Evaluations")

        # -------------------------------------------------
        # EVALUATE EACH STUDENT
        # -------------------------------------------------

        for student in students:

            student_answer = student["text"]

            student_answers = split_student_answers(student_answer)

            student_marks = {}

            total = 0

            evaluation_text = ""

            for q in ["Q1","Q2","Q3","Q4","Q5","Q6"]:
                student_ans = student_answers.get(q, "")

                if student_ans.strip() == "":
                    marks = 0
                    result = "No Answer"
                else:
                    # ✅ ONLY THIS LINE (RAG used here)
                    result = rag_chain(q, student_ans)

                    match = re.search(r"(\d+)/(\d+)", result)
                    marks = int(match.group(1)) if match else 0

                total += marks
                evaluation_text += f"\n\n{q}:\n{result}"
                match = re.search(r"Marks\s*:\s*(\d+)", result)

                if match:
                    marks = int(match.group(1))
                else:
                    marks = 0

                student_marks[q] = str(marks)

                total += marks

            st.subheader(f"Evaluation for {student['filename']}")
            st.write(evaluation_text)

            marks = f"{total}/80"

            results_table.append({

                "Department": department,
                "Subject": subject,
                "Subject Code": subject_code,
                "Exam Date": exam_date,

                "Student File": student["filename"],

                "Q1": student_marks.get("Q1","0"),
                "Q2": student_marks.get("Q2","0"),
                "Q3": student_marks.get("Q3","0"),
                "Q4": student_marks.get("Q4","0"),

                "Q5": student_marks.get("Q5","0"),
                "Q6": student_marks.get("Q6","0"),

                "Total Marks": marks
            })

    # -------------------------------------------------
    # CREATE DATAFRAME
    # -------------------------------------------------

    df = pd.DataFrame(results_table)

    # -------------------------------------------------
    # LEADERBOARD SORT
    # -------------------------------------------------

    try:

        df["Score"] = df["Total Marks"].str.replace("/80","").astype(int)

        df = df.sort_values(by="Score", ascending=False)

        df = df.drop(columns=["Score"])

    except:
        pass

    st.divider()

    # -------------------------------------------------
    # DASHBOARD
    # -------------------------------------------------

    st.subheader("📊 Evaluation Dashboard")

    col6, col7 = st.columns(2)

    with col6:
        st.metric("Total Students", len(df))

    with col7:
        st.metric("Evaluated Scripts", len(df))

    st.divider()

    # -------------------------------------------------
    # FINAL TABLE
    # -------------------------------------------------

    st.subheader("🏆 Final Student Evaluation Summary")

    st.dataframe(df, use_container_width=True)

    # -------------------------------------------------
    # DOWNLOAD CSV
    # -------------------------------------------------

    csv = df.to_csv(index=False)

    st.download_button(
        label="⬇️ Download Results as CSV",
        data=csv,
        file_name="student_evaluation_results.csv",
        mime="text/csv"
    )