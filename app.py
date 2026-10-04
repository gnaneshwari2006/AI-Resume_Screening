import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
import plotly.express as px

from resume_parser import extract_text
from skill_matcher import extract_skills

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)


# =========================
# PROFESSIONAL UI
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #6b7280;
    margin-bottom: 30px;
}

.dashboard-card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0,0,0,.05);
    margin-bottom: 20px;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #111827;
    margin-top: 25px;
    margin-bottom: 15px;
}

.stButton > button {
    border-radius: 10px;
    border: none;
    background-color: #2563eb;
    color: white;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

[data-testid="stFileUploader"] {
    background: white;
    border-radius: 12px;
    padding: 10px;
    border: 1px solid #dbe1ea;
}

[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 3px 12px rgba(0,0,0,.04);
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">AI Resume Screening System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Intelligent resume analysis and candidate-job matching platform</div>',
    unsafe_allow_html=True
)

# Session state
if "results" not in st.session_state:
    st.session_state.results = []

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Home", "Resume Screening", "Analytics"]
)

if st.sidebar.button("🗑️ Clear All Results"):
    st.session_state.results = []
    st.rerun()

# ---------------- HOME ----------------
if page == "Home":
    st.markdown("""
    <div class="dashboard-card">
        <h2>🚀 Smart Recruitment Starts Here</h2>
        <p style="font-size:17px;color:#6b7280;">
        Upload resumes, analyze candidate skills, compare them with job requirements,
        and identify the strongest candidates through automated screening.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)

    h1, h2, h3 = st.columns(3)
    with h1:
        st.markdown("""
        <div class="dashboard-card">
            <h3>📄 01. Upload</h3>
            <p>Upload candidate resumes in PDF or DOCX format.</p>
        </div>
        """, unsafe_allow_html=True)
    with h2:
        st.markdown("""
        <div class="dashboard-card">
            <h3>🔍 02. Analyze</h3>
            <p>Extract skills and compare them with job requirements.</p>
        </div>
        """, unsafe_allow_html=True)
    with h3:
        st.markdown("""
        <div class="dashboard-card">
            <h3>📊 03. Rank</h3>
            <p>Compare match scores, missing skills and candidate rankings.</p>
        </div>
        """, unsafe_allow_html=True)

    st.header("Welcome")
    st.write(
        "This application helps recruiters extract skills from resumes, "
        "compare them with a job description, calculate a match score, "
        "and analyze candidates."
    )

    results = st.session_state.results
    total = len(results)
    avg = sum(r["match_score"] for r in results) / total if total else 0
    best = max((r["match_score"] for r in results), default=0)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Resumes Screened", total)
    c2.metric("Average Match", f"{avg:.2f}%")
    c3.metric("Best Match", f"{best:.2f}%")
    c4.metric("Qualified (≥70%)", sum(r["match_score"] >= 70 for r in results))

    st.info("Go to **Resume Screening** to upload resumes and analyze candidates.")

# ---------------- SCREENING ----------------
elif page == "Resume Screening":
    st.header("🔎 Resume Screening")

    job_description = st.text_area(
        "Enter the job description:",
        height=220,
        placeholder=(
            "Example:\n\n"
            "We are looking for a Python Developer.\n\n"
            "Required skills:\n"
            "Python, SQL, Django, Flask, Pandas, AWS and Git."
        )
    )

    uploaded_files = st.file_uploader(
        "Upload PDF or DOCX resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if st.button("🚀 Analyze Resumes", type="primary"):
        if not job_description.strip():
            st.warning("Please enter a job description.")
        elif not uploaded_files:
            st.warning("Please upload at least one resume.")
        else:
            required_skills = extract_skills(job_description)

            if not required_skills:
                st.warning("No recognized skills were found in the job description.")
            else:
                st.success(f"{len(uploaded_files)} resume(s) uploaded successfully.")
                st.write("### Required Skills")
                st.info(", ".join(required_skills))

                # Remove previous results for the same batch so repeated clicks
                # don't create accidental duplicates.
                uploaded_names = {f.name for f in uploaded_files}
                st.session_state.results = [
                    r for r in st.session_state.results
                    if r["file_name"] not in uploaded_names
                ]

                batch_results = []

                for file in uploaded_files:
                    st.divider()
                    st.subheader(f"📄 {file.name}")

                    try:
                        resume_text = extract_text(file)
                    except Exception as e:
                        st.error(f"Could not read {file.name}: {e}")
                        continue

                    if not resume_text.strip():
                        st.warning("No text could be extracted from this resume.")
                        continue

                    resume_skills = extract_skills(resume_text)
                    matched = sorted(set(resume_skills) & set(required_skills))
                    missing = sorted(set(required_skills) - set(resume_skills))

                    score = (
                        len(matched) / len(required_skills) * 100
                        if required_skills else 0
                    )

                    if score >= 80:
                        status = "Highly Recommended"
                    elif score >= 70:
                        status = "Recommended"
                    elif score >= 50:
                        status = "Consider"
                    else:
                        status = "Not Recommended"

                    result = {
                        "file_name": file.name,
                        "match_score": round(score, 2),
                        "matched_count": len(matched),
                        "missing_count": len(missing),
                        "matched_skills": ", ".join(matched),
                        "missing_skills": ", ".join(missing),
                        "status": status,
                    }

                    batch_results.append(result)

                    with st.expander("View extracted resume text"):
                        st.text_area(
                            "Extracted Text",
                            resume_text,
                            height=250,
                            key=f"text_{file.name}"
                        )

                    c1, c2, c3 = st.columns(3)
                    c1.metric("Match Score", f"{score:.2f}%")
                    c2.metric("Matched Skills", len(matched))
                    c3.metric("Missing Skills", len(missing))

                    if status == "Highly Recommended":
                        st.success("🏆 " + status)
                    elif status == "Recommended":
                        st.success("✅ " + status)
                    elif status == "Consider":
                        st.warning("⚠️ " + status)
                    else:
                        st.error("❌ " + status)

                    st.progress(
                        int(score),
                        text=f"Candidate Match: {score:.2f}%"
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("### ✅ Matched Skills")
                        if matched:
                            st.success(", ".join(matched))
                        else:
                            st.info("No matching skills found.")

                    with col2:
                        st.write("### ❌ Missing Skills")
                        if missing:
                            st.error(", ".join(missing))
                        else:
                            st.success("No missing skills!")

                st.session_state.results.extend(batch_results)

                if batch_results:
                    st.success("Screening completed. Open **Analytics** to compare candidates.")

# ---------------- ANALYTICS ----------------
elif page == "Analytics":
    st.markdown('<div class="main-title">Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Candidate performance and skill-matching insights</div>',
        unsafe_allow_html=True
    )

    results = st.session_state.results

    if not results:
        st.info("No screening results available yet. Analyze resumes first.")
    else:
        df = pd.DataFrame(results).sort_values(
            "match_score", ascending=False
        ).reset_index(drop=True)

        # Ranking
        df.insert(0, "Rank", range(1, len(df) + 1))

        avg = df["match_score"].mean()
        best = df["match_score"].max()
        qualified = int((df["match_score"] >= 70).sum())

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Candidates", len(df))
        c2.metric("Average Score", f"{avg:.2f}%")
        c3.metric("Best Score", f"{best:.2f}%")
        c4.metric("Qualified", qualified)

        st.subheader("🏆 Candidate Ranking")
        display_df = df[
            ["Rank", "file_name", "match_score", "matched_count", "missing_count", "status"]
        ].rename(columns={
            "file_name": "Candidate",
            "match_score": "Match Score (%)",
            "matched_count": "Matched Skills",
            "missing_count": "Missing Skills",
            "status": "Recommendation"
        })
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Score chart
        st.subheader("📈 Match Score by Candidate")
        fig = px.bar(
            df,
            x="file_name",
            y="match_score",
            text="match_score",
            labels={"file_name": "Candidate", "match_score": "Match Score (%)"},
            title="Candidate Match Scores"
        )
        fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig.update_yaxes(range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

        # Matched vs missing
        st.subheader("🔄 Matched vs Missing Skills")
        skill_df = pd.DataFrame({
            "Category": ["Matched Skills", "Missing Skills"],
            "Count": [
                int(df["matched_count"].sum()),
                int(df["missing_count"].sum())
            ]
        })
        fig2 = px.pie(
            skill_df,
            names="Category",
            values="Count",
            hole=0.45,
            title="Overall Skill Coverage"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Individual candidate details
        st.subheader("🔍 Candidate Details")
        selected = st.selectbox("Select candidate", df["file_name"].tolist())
        row = df[df["file_name"] == selected].iloc[0]

        d1, d2 = st.columns(2)
        with d1:
            st.write("### ✅ Matched Skills")
            st.success(row["matched_skills"] or "None")
        with d2:
            st.write("### ❌ Missing Skills")
            st.error(row["missing_skills"] or "None")

        # Download
        export_df = df[
            ["Rank", "file_name", "match_score", "matched_count",
             "missing_count", "matched_skills", "missing_skills"]
        ]
        csv = export_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Screening Results (CSV)",
            data=csv,
            file_name="resume_screening_results.csv",
            mime="text/csv"
        )

