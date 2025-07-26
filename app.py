import streamlit as st
from dotenv import load_dotenv
from prompts import generate_questions
from utils import store_candidate_data, analyze_sentiment
from config import GREETING_MESSAGE, END_MESSAGE
import time

load_dotenv()
st.set_page_config(page_title="TalentScout Assistant", layout="centered")

if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.candidate = {}

# Chat style title (logo removed)
with st.chat_message("assistant"):
    st.markdown(GREETING_MESSAGE)

# Step 1: Candidate info form
if st.session_state.step == 1:
    with st.chat_message("user"):
        st.subheader("👤 Candidate Information")
        st.session_state.candidate['name'] = st.text_input("Full Name")
        st.session_state.candidate['email'] = st.text_input("Email Address")
        st.session_state.candidate['phone'] = st.text_input("Phone Number")
        st.session_state.candidate['experience'] = st.selectbox("Years of Experience", [0, 1, 2, 3, 4, "5+"])
        st.session_state.candidate['position'] = st.text_input("Desired Position")
        st.session_state.candidate['location'] = st.text_input("Current Location")
        tech_stack = st.text_input("Tech Stack (comma-separated)")

    if st.button("Next"):
        if all(st.session_state.candidate.values()) and tech_stack:
            st.session_state.candidate['tech_stack'] = tech_stack
            store_candidate_data(st.session_state.candidate)
            st.session_state.step = 2
        else:
            st.warning("Please complete all fields.")

# Step 2: GPT Question Generation
elif st.session_state.step == 2:
    with st.chat_message("assistant"):
        st.subheader("🧠 Technical Questions")
        experience = st.session_state.candidate.get("experience")
        tech_stack = st.session_state.candidate.get("tech_stack")
        questions = generate_questions(tech_stack, experience)
        st.markdown(questions)

    with st.chat_message("user"):
        user_answer = st.text_area("Answer any one question briefly (optional):")
        if st.button("Submit Answer"):
            sentiment = analyze_sentiment(user_answer)
            with st.chat_message("assistant"):
                if sentiment > 0.3:
                    st.success("✅ You sound confident! Keep it up.")
                elif sentiment < -0.3:
                    st.warning("🤔 You seem unsure. It's okay, stay relaxed.")
                else:
                    st.info("👍 Thanks for your response!")

    if st.button("End Conversation"):
        with st.chat_message("assistant"):
            st.success(END_MESSAGE)
        st.session_state.step = 3

# Step 3: Thank You
elif st.session_state.step == 3:
    st.balloons()
