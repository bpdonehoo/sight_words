import streamlit as st
import os
import glob
import pathlib
import random
import time

def load_secrets():
    SECRETS_FILE = pathlib.Path.cwd() / 'secrets.env'
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, 'r') as f:
            return dict(tuple(line.replace('\n', '').split('=')) for line in f.readlines() if not line.startswith('#'))
    else:
        return os.environ


def process_csv_TTS(INPUT_FILE, AUDIO_PATH):
    import boto3
    import csv

    INPUT_FILE = pathlib.Path.cwd() / 'data' / 'sight_words.csv'
    secrets_dict = load_secrets()

    polly_client = boto3.Session(
                    aws_access_key_id=secrets_dict['ACCESS_KEY'],                     
                    aws_secret_access_key=secrets_dict['SECRET_KEY'],
                    region_name='us-west-2').client('polly')

    with open(INPUT_FILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # Ignore Header Row
                line_count += 1
            else:
                current_word = row[0]
                print(f'Current Word is: {current_word}')
                
                if not os.path.exists(f'{AUDIO_PATH}/{current_word}.mp3'):
                    response = polly_client.synthesize_speech(VoiceId='Joanna',
                                                            OutputFormat='mp3',
                                                            Text=current_word,
                                                            Engine='neural')
                    file = open(f'{AUDIO_PATH}/{current_word}.mp3', 'wb')
                    file.write(response['AudioStream'].read())
                    file.close()

                line_count += 1
    return None


def select_words_from_dir(AUDIO_PATH, number_of_words):
    file_list = glob.glob(f'{AUDIO_PATH}/*.mp3')
    file_count = len(file_list)

    selected_numbers = random.sample(range(1, file_count+1), number_of_words)
    selected_words = [pathlib.Path(file_list[x]).stem for x in selected_numbers]
    return selected_words


def play_mp3(mp3_path):
    from pygame import mixer
    mixer.init()
    mixer.music.load(mp3_path)
    mixer.music.play()


def execute_sight_words(AUDIO_PATH):
    if 'selected_words' not in st.session_state:
            st.session_state.selected_words = select_words_from_dir(AUDIO_PATH, 5)
            st.session_state.chosen_word = random.choice(st.session_state.selected_words)
            st.session_state.total_answers = 0
            st.session_state.correct_answers = 0 
            
    st.title('Sight Words App')

    audio_placeholder = st.empty()
    audio_player = audio_placeholder.audio(str(AUDIO_PATH / f'{st.session_state.chosen_word}.mp3'))

    radio_placeholder = st.empty()
    radio_btn = radio_placeholder.radio('Select the Correct Word:', st.session_state.selected_words)

    submit = st.button('Submit Answer')

    text_placeholder = st.empty()

    if submit and radio_btn == st.session_state.chosen_word:
        text_placeholder.text('Correct Answer!')
        time.sleep(0.5)
        text_placeholder.empty()

        st.session_state.selected_words = select_words_from_dir(AUDIO_PATH, 5)
        st.session_state.chosen_word = random.choice(st.session_state.selected_words)
        st.session_state.total_answers += 1
        st.session_state.correct_answers += 1

        radio_placeholder.radio('Select the Correct Word:', st.session_state.selected_words)

        audio_player = audio_placeholder.audio(str(AUDIO_PATH / f'{st.session_state.chosen_word}.mp3'))
    elif submit:
        text_placeholder.text('Incorrect, Try Again!')
        st.session_state.total_answers += 1
    else:
        pass
    
    st.write(f'Total Guesses: {st.session_state.total_answers}')
    st.write(f'Total Correct: {st.session_state.correct_answers}')