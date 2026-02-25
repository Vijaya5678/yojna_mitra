import os
import streamlit as st

from recommender import UserProfile, load_yojnas, recommend_yojnas, asdict_user
from gemini_helper import summarize


# ---------------- UI Styling ----------------
st.set_page_config(page_title="Yojna Mitra", page_icon="🪙", layout="centered")
st.markdown("""
<style>
/* Cards */
.y-card {
  border: 1px solid rgba(0,0,0,0.1);
  background: #ffffff;
  border-radius: 12px;
  padding: 14px 16px;
  margin-bottom: 10px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.04);
}
.y-meta { color: #667085; font-size: 13px; margin-top: 6px; }
.y-pill { display:inline-block; padding: 2px 8px; background: #eef2ff; color:#3730a3; border-radius: 999px; margin-right:6px; font-size:12px;}
.y-title { margin: 0 0 4px 0; font-weight: 700; }
.y-section-title { font-weight: 600; margin: 10px 0 4px 0; }
</style>
""", unsafe_allow_html=True)

st.title("Yojna Mitra")
st.caption("Find the best Indian Government Schemes tailored to you — quick, simple, offline-friendly data.")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("About Yojna Mitra")
    st.write("""
**Yojna Mitra** helps you discover the most relevant Government of India schemes
based on your age, gender, income, state, and basic profile.

It quickly matches your details with a list of verified schemes and shows you
only those you may be eligible for. The goal is to make it easier for every
citizen to understand which benefits they can apply for — without searching
across multiple websites.

Just enter your details and let Yojna Mitra guide you.
    """)

    st.divider()
    
# ---------------- Form ----------------
col1, col2 = st.columns([1, 1])
with st.form("yojna_form"):
    name = st.text_input("Name (optional)", "")
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Age", min_value=0, max_value=120, step=1, value=28)
    with c2:
        gender = st.selectbox("Gender", ["female", "male", "other"], index=0)
    with c3:
        income = st.number_input("Annual Income (INR)", min_value=0, step=5000, value=300000)

    c4, c5 = st.columns(2)
    with c4:
        state = st.text_input("State Code (e.g., KA, MH, DELHI)", value="KA")
    with c5:
        occupation = st.text_input("Occupation (e.g., farmer, student)", value="")

    top_n = st.slider("Max recommendations to show", 1, 20, 8)
    submitted = st.form_submit_button("Get Recommendations", use_container_width=True)

if submitted:
    # Load data and run matching
    yojnas = load_yojnas()
    user = UserProfile(
        name=name,
        age=age,
        gender=gender,
        income=income,
        state=state,
        occupation=occupation,
    )
    matches = recommend_yojnas(user, yojnas, top_n=top_n)

    if not matches:
        st.warning("No matching schemes found. Try adjusting age/income/gender/state.")
    else:
        st.subheader("Recommended Schemes")
        for s in matches:
            states = s.get("states", ["ALL"])
            tags = s.get("tags", [])
            col = st.container()
            with col:
                st.markdown(f"""
<div class="y-card">
  <div class="y-title">{s['name']}</div>
  <div class="y-meta">{s.get('category','')} • Income limit: {('No limit' if s['incomeLimit']==0 else s['incomeLimit'])} • Age: {s['ageRange'][0]}–{s['ageRange'][1]}</div>
  <div style="margin-top:8px;">{s.get('description','')}</div>
  <div class="y-meta" style="margin-top:8px;">
    <span class="y-pill">{'ALL India' if 'ALL' in [stt.upper() for stt in states] else ', '.join(states)}</span>
    {"".join(f'<span class="y-pill">{t}</span>' for t in tags)}
  </div>
</div>
""", unsafe_allow_html=True)

        # Optional Gemini summary
        ai_summary = summarize(asdict_user(user), matches[:5])
        if ai_summary:
            st.subheader("AI Summary (Gemini)")
            st.info(ai_summary)

        # Debug / transparency (optional)
        with st.expander("See input profile"):
            st.json(asdict_user(user))
        with st.expander("See raw matched items"):
            st.json(matches)