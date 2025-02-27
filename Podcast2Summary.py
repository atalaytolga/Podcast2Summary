import whisper
from transformers import pipeline
import streamlit as st
import os


# Streamlit UI
st.title("Podcast2Summary - AI Podcast Summarizer")
podcast_url = st.text_input("Enter Podcast URL:", placeholder="https://...")


# Model selection
st.sidebar.header("Model Selection")

# Whisper model selection
whisper_model_choice = st.sidebar.radio(
    "Choose a Whisper model:",
    ("tiny", "base", "medium", "large"),
    index=1
)


# Summarization model selection
summarization_model = st.sidebar.radio(
    "Choose a Summarization model:",
    ("t5-small", "t5-base", "bart-large"),
    index=0
)


# Function to transcribe audio
def transcribe_audio(audio_file):
    result = whisper_model.transcribe(audio_file)
    return result["text"]

# Function to summarize text
def summarize_text(text, max_length=150):
    summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
    return summary[0]["summary_text"]



# Upload audio file
uploaded_file = st.file_uploader("Or Alternatively, Upload a Podcast (MP3/WAV)", type=["mp3", "wav"])

if uploaded_file is not None:
    # Load selected Whisper model
    whisper_model = whisper.load_model(whisper_model_choice)

    # Load the selected summarization model
    summarizer = pipeline("summarization", model=summarization_model)

    # Save uploaded file temporarily
    file_path = os.path.join("temp_audio.mp3")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.write("Transcribing audio...")
    transcript = transcribe_audio(file_path)
    st.text_area("Transcribed Text:", transcript, height=200)
    
    st.write("Summarizing Podcast...")
    summary = summarize_text(transcript)
    st.text_area("Podcast Summary:", summary, height=150)
    
    st.success("Done! Your podcast summary is ready.")

