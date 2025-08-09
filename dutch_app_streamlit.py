import streamlit as st
import random
import json
import requests
from pathlib import Path
from gtts import gTTS
import tempfile
import os
from bs4 import BeautifulSoup

# Local progress file
PROGRESS_FILE = Path("progress.json")

# CEFR-aligned vocabulary sources (example links for A0–B1)
WORDLIST_URLS = {
    "A0-A2": "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/nl/nl_50k.txt",
    "B1": "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/nl/nl_full.txt"
}

def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"correct": 0, "total": 0}

def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f)

def fetch_vocab(level="A0-A2", limit=20):
    """Fetch Dutch words from an online frequency list and return a sample."""
    try:
        url = WORDLIST_URLS[level]
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        words = [line.split()[0] for line in resp.text.splitlines() if line.strip()]
        return random.sample(words[:1000], limit)  # Pick from top 1000 for common words
    except Exception as e:
        st.error(f"Could not fetch vocabulary: {e}")
        return []

def fetch_phrases():
    ''' Test phrase scraper '''
    url = "https://www.colanguage.com/basic-words-and-phrases-dutch"
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    phrases = []
    table = soup.find("table")
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        en = cols[0].text.strip()
        nl = cols[1].text.strip()
        phrases.append({"nl": nl, "en": en})
    print(phrases)
    return phrases


def get_pronunciation(word):
    """Generate pronunciation audio using Google TTS."""
    try:
        tts = gTTS(word, lang="nl")
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp.name)
        return tmp.name
    except Exception as e:
        print("Getting pronunciation failed!: {}\n", e)
        return None

# Streamlit UI
st.set_page_config(page_title="Learn Dutch", page_icon="🇳🇱", layout="centered")
st.title("🇳🇱 Learn Dutch — Pass Your A0–A2 & B1 Exams")

level = st.selectbox("Choose your level:", ["A0-A2", "B1"])
if "vocab" not in st.session_state:
    st.session_state.vocab = fetch_vocab(level)
    st.session_state.progress = load_progress()
    st.session_state.current_word = None

if st.button("New Word"):
    st.session_state.current_word = random.choice(st.session_state.vocab)

if st.session_state.current_word:
    dutch_word = st.session_state.current_word
    st.subheader(f"What does **{dutch_word}** mean in English?")
    answer = st.text_input("Your answer:")

    if st.button("Check Answer"):
        # For now we use an online dictionary API
        try:
            dict_resp = requests.get(f"https://api.mymemory.translated.net/get?q={dutch_word}&langpair=nl|en", timeout=10)
            meaning = dict_resp.json().get("responseData", {}).get("translatedText", "Unknown")
        except Exception as e:
            meaning = "Unknown"

        if answer.lower().strip() == meaning.lower().strip():
            st.success("✅ Correct!")
            st.session_state.progress["correct"] += 1
        else:
            st.error(f"❌ Wrong. It means '{meaning}'.")
        st.session_state.progress["total"] += 1
        save_progress(st.session_state.progress)

        audio_path = get_pronunciation(dutch_word)
        if audio_path:
            st.audio(audio_path, format="audio/mp3")

st.write(f"**Progress:** {st.session_state.progress['correct']} / {st.session_state.progress['total']} correct")

# External resources for grammar & exam prep
st.markdown("### 📚 Extra Resources")
st.markdown("""
- [Nederlandse Taalunie — Official Dutch Grammar](https://taalunie.org/)
- [Duolingo Dutch](https://www.duolingo.com/course/nl/en/Learn-Dutch)
- [Oefenen.nl — Dutch for Beginners](https://www.oefenen.nl/)
- [Staatsexamen NT2 Info](https://www.staatsexamensnt2.nl/)
""")
