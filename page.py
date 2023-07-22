import streamlit as st
from ai_components import create_ques_ans,report

def app():
    tab1= st.tabs(["Give a quick quiz!"])

    st.title("Let's test your knowledge!")
    st.header("Attempt this multiple choice based quiz and test your knowledge in all levels of learning!")

    session_state = st.session_state
    if "quiz_data" not in session_state:
        session_state.quiz_data = None
    if "score" not in session_state:
        session_state.score = 0
    
    topic_placeholder = st.empty()

    button=st.empty()
    
    if session_state.quiz_data is None:
        
        topic = topic_placeholder.text_input("topic")
        
        if button.button("Generate"):
            try:
                    session_state.quiz_data = create_ques_ans( topic)
                    
                    topic_placeholder.empty()
            except Exception as e :
                    st.error("Please enter some topic")
    if session_state.quiz_data:
        questions = session_state.quiz_data[0]
        options = session_state.quiz_data[1]
        answers = session_state.quiz_data[2]
    
    ans = []
    if session_state.quiz_data:
        button.empty()
        with st.form(key='quiz'):
            question_placeholders = []
            for i, quest in enumerate(questions):
                st.write(f"{i+1}. {quest}")
                question_placeholder = st.empty()
                question_placeholders.append(question_placeholder)
                options_= options[i]

                choice = st.radio("", options_, key=i)
                if choice:
                    ans.append(choice)
            if session_state.quiz_data:
                submitted = st.form_submit_button("Submit")
            else:
                submitted = False
            if submitted:
                session_state.score=0
                for i, user_input in enumerate(answers):
                    question_placeholder = question_placeholders[i]
                    if ans[i] == user_input:
                        session_state.score+=1
                        question_placeholder.success("Correct  Answer!")
                    if ans[i] != user_input:
                        question_placeholder.error(f" Wrong! , right answer is {answers[i]}")
                st.success("Test Score - " + str(session_state.score))
                st.success(f'{report([questions,ans],session_state.score,len(answers))}')
        if session_state.quiz_data :
            new_quiz = st.button("new quiz")
            if new_quiz:
                session_state.quiz_data = None
                session_state.score = 0
                st.experimental_rerun()
app()