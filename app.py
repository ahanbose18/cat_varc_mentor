import streamlit as st
from rc_generator import generate_rc_passage
from evaluator import evaluate_user_answers
from datetime import datetime
import time


st.title("AI-Powered Reading Comprehension Passage Generator")
st.subheader("Generate CAT-style RC Passages with Questions")
# Google Form URL
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSd893LWEpBFtkHun6m19U2djFrkUM-N0CkIGh-pcghHgE4ZbA/viewform?usp=sharing&ouid=113708083278017820025"

# Display the hyperlink
st.write(f'<a href="{form_url}" target="_blank">Please share your feedback here</a>', unsafe_allow_html=True)
topic = st.text_input("Enter a topic (e.g., Globalization, AI, Ethics)")
difficulty = st.selectbox("Choose difficulty", ["Easy", "Moderate", "Hard"])
if difficulty == "Easy":
    fk_scale = "4-6"
elif difficulty == "Moderate":
    fk_scale = "7-9"
else:
    fk_scale = "10-12"
passage_length = st.selectbox("Choose Passage Length", ["200","500","900"])
st.write("Developed by [Ahan Bose]. Reach out to me on [LinkedIn](https://www.linkedin.com/in/ahan-bose-spjimr/)")
if st.button("Generate RC", key="generate_rc_button"):
    output = generate_rc_passage(topic, fk_scale, passage_length)
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
    st.subheader("Evaluate Your Answers")
    answers = [st.selectbox(f"Your Answer for Q{i}:", ["A", "B", "C", "D"], key=f"q{i}") for i in range(1, 6)]
    
    if st.button("Evaluate"):
        results = evaluate_user_answers(st.session_state.generated_output, answers)
        for res in results:
            st.write(res)
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
        time.sleep(5)

    if st.button("Reveal Explanation", key="reveal_explaination_button"):
        st.markdown("### 📌Explaination")
    
        for i, line in enumerate(st.session_state.generated_output.split("\n")):
            if line.strip().startswith("Explanation:"):
                st.write(f"Q{i+1}: {line.split(':')[1].strip()}")
        else:
            st.warning("Generate a passage first.")
        st.stop()


else:
    st.warning("Generate a passage first to evaluate answers or reveal correct answers.")

st.stop()