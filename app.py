import streamlit as st
import pathlib
from sight_words import sight_words
from sight_words import division_estimation

AUDIO_PATH = pathlib.Path.cwd() / 'data' / 'audio'

sidebar_radio = st.sidebar.radio("Choose an Application:", ("Sight Words", "Division Estimation"))

if sidebar_radio == 'Sight Words':
    sight_words.execute_sight_words(AUDIO_PATH)

elif sidebar_radio == 'Division Estimation':
    division_estimation.execute_division_estimation()