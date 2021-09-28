from attr import s
import streamlit as st
import random
import math
import time


def execute_math_drills():

    if 'answer' not in st.session_state:
        st.session_state.question_type = random.choice(['multiplication', 'division'])
        st.session_state.divisor = random.randint(1,99) * random.choice([10, 100])
        st.session_state.quotient = random.randint(2,9) * random.choice([10, 100])
        st.session_state.dividend = st.session_state.divisor * st.session_state.quotient
        if st.session_state.question_type == 'multiplication':
            st.session_state.answer = st.session_state.dividend
        elif st.session_state.question_type == 'division':
            st.session_state.answer = st.session_state.quotient
        else:
            pass
        st.session_state.total_answers = 0
        st.session_state.correct_answers = 0 
    
    st.title('Math Drills')
    st.subheader('Answer the following questions:')

    col1, col2, col3 = st.columns(3)

    with col2:
        markdown_placeholder = st.empty()
        if st.session_state.question_type == 'multiplication':
            markdown_text = fr'{st.session_state.divisor}x{st.session_state.quotient}'
        elif st.session_state.question_type == 'division':
            markdown_text = fr'$\frac{{{st.session_state.dividend}}}{{{st.session_state.divisor}}}$'
        markdown_placeholder.markdown(markdown_text)
    

    answer_placeholder = st.empty()
    answer_input = answer_placeholder.number_input('Answer', key='answer0')
    
    submit = st.button('Submit Answer')
    text_placeholder = st.empty()

    if submit and answer_input == st.session_state.answer:
        text_placeholder.text(f'Correct!')
        time.sleep(1)
        text_placeholder.empty()

        answer_placeholder.empty()
        answer_placeholder.number_input('Answer', key='answer1')

        st.session_state.question_type = random.choice(['multiplication', 'division'])
        st.session_state.divisor = random.randint(1,99) * random.choice([10, 100])
        st.session_state.quotient = random.randint(2,9) * random.choice([10, 100])
        st.session_state.dividend = st.session_state.divisor * st.session_state.quotient
        if st.session_state.question_type == 'multiplication':
            st.session_state.answer = st.session_state.dividend
        elif st.session_state.question_type == 'division':
            st.session_state.answer = st.session_state.quotient
        else:
            pass
        st.session_state.total_answers += 1
        st.session_state.correct_answers += 1

        if st.session_state.question_type == 'multiplication':
            markdown_text = fr'{st.session_state.divisor}x{st.session_state.quotient}'
        elif st.session_state.question_type == 'division':
            markdown_text = fr'$\frac{{{st.session_state.dividend}}}{{{st.session_state.divisor}}}$'
        markdown_placeholder.markdown(markdown_text)

    elif submit:
        text_placeholder.text('Incorrect, Try Again!')
        st.session_state.total_answers += 1
    else:
        pass
    
    st.write(f'Total Guesses: {st.session_state.total_answers}')
    st.write(f'Total Correct: {st.session_state.correct_answers}')