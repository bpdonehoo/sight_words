import streamlit as st
import random
import math
import time

def execute_division_estimation():
    if 'dividend' not in st.session_state:
            st.session_state.dividend = random.randint(1000,9999)
            st.session_state.divisor = random.randint(11,99)
            st.session_state.answer = st.session_state.dividend / st.session_state.divisor
            st.session_state.lower_bound = int(math.floor(st.session_state.answer / 10.0)) * 10
            st.session_state.upper_bound = int(math.ceil(st.session_state.answer / 10.0)) * 10
            st.session_state.total_answers = 0
            st.session_state.correct_answers = 0 

    st.title('Division Estimation Drills')
    st.subheader('Find the Lower and Upper Range Estimate for the Following:')
    col1, col2, col3 = st.columns(3)

    with col2:
        markdown_placeholder = st.empty()
        markdown_text = fr'$\frac{{{st.session_state.dividend}}}{{{st.session_state.divisor}}}$'
        markdown_placeholder.markdown(markdown_text)
    
    col4, col5 = st.columns(2)
    with col4:
        lower_placeholder = st.empty()
        lower_bound_input = lower_placeholder.number_input('Lower Bound Estimate', key='lower')
    with col5:
        upper_placeholder = st.empty()
        upper_bound_input = upper_placeholder.number_input('Upper Bound Estimate', key='upper')
    
    submit = st.button('Submit Answer')
    text_placeholder = st.empty()

    if submit and lower_bound_input == st.session_state.lower_bound and upper_bound_input == st.session_state.upper_bound:
        text_placeholder.text(f'Correct Range! The Full Answer is: {round(st.session_state.answer,2)}')
        time.sleep(1)
        text_placeholder.empty()

        lower_placeholder.empty()
        lower_placeholder.number_input('Lower Bound Estimate', key='lower1')
        upper_placeholder.empty()
        upper_placeholder.number_input('Upper Bound Estimate', key='upper2')

        st.session_state.dividend = random.randint(1000,9999)
        st.session_state.divisor = random.randint(11,99)
        st.session_state.answer = st.session_state.dividend / st.session_state.divisor
        st.session_state.lower_bound = int(math.floor(st.session_state.answer / 10.0)) * 10
        st.session_state.upper_bound = int(math.ceil(st.session_state.answer / 10.0)) * 10
        st.session_state.total_answers += 1
        st.session_state.correct_answers += 1

        markdown_text = fr'$\frac{{{st.session_state.dividend}}}{{{st.session_state.divisor}}}$'
        markdown_placeholder.markdown(markdown_text)

    elif submit:
        text_placeholder.text('Incorrect, Try Again!')
        st.session_state.total_answers += 1
    else:
        pass
    
    st.write(f'Total Guesses: {st.session_state.total_answers}')
    st.write(f'Total Correct: {st.session_state.correct_answers}')
