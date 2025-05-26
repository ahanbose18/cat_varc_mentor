import streamlit as st
from rc_generator import generate_rc_passage
from evaluator import evaluate_user_answers
from datetime import datetime
import time

st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFF2EB;  /* Light beige background */
    }

    .stHeading > h1 {
        color: #096B68;  /* Dark teal */
        font-family: 'Arial', sans-serif;
        font-weight: bold; 
        font-size: 36px; 
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .stButton > button {
        background-color: #4E71FF !important;  /* Indigo */
        color: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border: none !important;
    }

    /* Button hover effect */
    .stButton > button:hover {
        background-color: #BBFBFF !important;  /* Lighter indigo */
        color: #096B68 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("AI-Powered Reading Comprehension Passage Generator")
st.subheader("Generate CAT-style RC Passages with Questions")
topic = st.text_input("Enter a topic (e.g., Globalization, AI, Ethics)")
difficulty = st.selectbox("Choose difficulty", ["Easy", "Moderate", "Hard"])
passage_length = st.selectbox("Choose Passage Length", ["200","500","900"])

if st.button("Generate RC", key="generate_rc_button"):
    output = generate_rc_passage(topic, difficulty, passage_length)
    st.session_state.generated_output = output
    #st.text_area("RC Passage + Questions", output, height=500)
    # Remove answer lines from display version
    st.session_state.start_time = datetime.now()
    st.session_state.timer_running = True  # new flag

    lines = output.split("\n")
    visible_lines = [line for line in lines if (not line.strip().startswith("Answer:") and not line.strip().startswith("Explanation:"))]
    visible_output = "\n".join(visible_lines)
    st.session_state.visible_output = visible_output

    #st.text_area("Visible RC Passage + Questions", visible_output, height=500)


if 'generated_output' in st.session_state:

    st.text_area("RC Passage + Questions", st.session_state.visible_output, height=500)

    #Keeps track of the timer
    if 'start_time' in st.session_state and st.session_state.get('timer_running', False):
        elapsed = datetime.now() - st.session_state.start_time
        minutes, seconds = divmod(elapsed.total_seconds(), 60)
        st.markdown(f"⏱️ **Time Elapsed:** {int(minutes)} minutes {int(seconds)} seconds")

        # # Trigger a rerun every second
        # time.sleep(1)
        # st.rerun()

    if st.button("Reveal Answer", key="reveal_answer_button"):
        st.session_state.timer_running = False
        
        end_time = datetime.now()
        duration = end_time - st.session_state.start_time
        minutes, seconds = divmod(duration.total_seconds(), 60)
        st.success(f"✅ Time Taken: {int(minutes)} minutes {int(seconds)} seconds")
        st.markdown("### 📌 Correct Answers")
        for i, line in enumerate(st.session_state.generated_output.split("\n")):
            if line.strip().startswith("Answer:"):
                st.write(f"Q{i+1}: {line.split(':')[1].strip()}")
        else:
            st.warning("Generate a passage first.")
        time.sleep(10)
    if st.button("Reveal Explaination", key="reveal_explaination_button"):
        st.markdown("### 📌Explaination")
        # explanations = explain_answers(st.session_state.generated_output)
        # for exp in explanations:
        #     st.write(exp)
        for i, line in enumerate(st.session_state.generated_output.split("\n")):
            if line.strip().startswith("Explanation:"):
                st.write(f"Q{i+1}: {line.split(':')[1].strip()}")
        else:
            st.warning("Generate a passage first.")
        exit()

    #st.markdown(f"⏱️ **Time Elapsed:** {int(minutes)} minutes {int(seconds)} seconds")

      
    #Trigger a rerun every second
    time.sleep(1)
    st.rerun()
else:
    st.warning("Generate a passage first to evaluate answers or reveal correct answers.")