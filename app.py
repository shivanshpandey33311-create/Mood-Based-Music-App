import pickle
with open("emotion_model.pkl", "rb") as f:
    emotion_model = pickle.load(f)

with open("tfidf_vectorizer 2.pkl", "rb") as f:
    vectorizer = pickle.load(f)
    
import streamlit as st
from spotify_api import get_songs

st.title("🎧 Mood-Based Music Recommendation")

user_text = st.text_area("Write how you feel today:")

if st.button("Detect Emotion & Recommend"):
    if user_text.strip() == "":
        st.warning("Please write something first!")
    else:
        
        X_vec = vectorizer.transform([user_text])
        
        
        probs = model.predict_proba(X_vec)[0]
        emotions = model.classes_
        
        
        top_idx = probs.argmax()
        detected_emotion = emotions[top_idx]
        
        st.success(f"Detected Emotion: {detected_emotion}")
        
        
        songs = get_songs(detected_emotion)
        
        st.subheader("Recommended Songs")
        for song in songs:
            st.markdown(f"*{song['name']}* - {song['artist']}")
            st.markdown(f"[Listen on Spotify]({song['url']})")