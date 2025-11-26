import os
import requests
import streamlit as st
import google.generativeai as genai

# -------------------------
# CONFIG
# -------------------------
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

# System Instructions EXACT as requested
SYSTEM_INSTRUCTIONS = """
You are a movie fan who loves spotting hidden Easter eggs, references, and fun details in films.
When someone gives you a movie or scene, give 5–10 different Easter eggs in one message, numbered or bulleted.
Each Easter egg should be concise, human-like, and enthusiastic. Use emojis naturally.
Don't repeat phrases, and keep it friendly and casual.
"""

model = genai.GenerativeModel(
    "gemini-2.0-flash",
    system_instruction=SYSTEM_INSTRUCTIONS
)

st.set_page_config(page_title="Movie Easter Egg Lens", page_icon="🔍", layout="centered")

# -------------------------
# HEADER
# -------------------------
st.markdown("<h1 style='text-align:center;'>🔍 Movie Easter Egg Lens</h1>", unsafe_allow_html=True)

st.markdown("""
Ask about any movie you would like to find Easter eggs about,  
for example **Harry Potter**, **Inception**, or **Interstellar**,  
to get multiple hidden Easter eggs and fun movie secrets! 😎
""")

# -------------------------
# EXAMPLES
# -------------------------
st.subheader("💡 Try these:")
examples = [
    "What hidden stuff is in the first Harry Potter movie?",
    "Inception's spinning top scene – any cool Easter eggs?",
    "Any fun secrets in Interstellar's tesseract scene?",
    "Quidditch scenes in Harry Potter – anything I missed?",
    "Dream layers in Inception – hidden details?",
    "Interstellar – subtle things Nolan put in the movie?"
]
for ex in examples:
    st.markdown(f"- {ex}")

st.markdown("---")

# -------------------------
# TMDB POSTER FETCH
# -------------------------
def fetch_movie_poster(movie_name):
    if not TMDB_API_KEY:
        return None

    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    res = requests.get(url).json()

    if "results" not in res or len(res["results"]) == 0:
        return None

    poster_path = res["results"][0].get("poster_path")
    if not poster_path:
        return None

    return f"https://image.tmdb.org/t/p/w500{poster_path}"

# -------------------------
# MAIN FUNCTION — ONE CALL
# -------------------------
def generate_easter_eggs(user_query):
    try:
        chat = model.start_chat(history=[])
        response = chat.send_message(user_query)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {e}"

# -------------------------
# CHAT UI
# -------------------------
st.subheader("🎬 Ask About a Movie or Scene")

user_query = st.text_input("Your question about Easter eggs:")

# Store chat history in session_state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("🔍 Find Easter Eggs"):
    if user_query.strip():
        # Get Easter eggs (ONE Gemini call)
        answer = generate_easter_eggs(user_query)

        # Fetch movie poster
        poster_url = fetch_movie_poster(user_query)

        # Store newest on top
        st.session_state.chat_history.insert(0, {
            "user": user_query,
            "assistant": answer,
            "poster": poster_url
        })

# -------------------------
# DISPLAY CHAT HISTORY (newest first)
# -------------------------
for chat in st.session_state.chat_history:
    st.markdown("### You")
    st.write(chat["user"])

    st.markdown("### 🥚 Easter Eggs")
    
    if chat["poster"]:
        st.image(chat["poster"], width=250)

    st.write(chat["assistant"])
    st.markdown("---")

# -------------------------
# FOOTER
# -------------------------
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🎬 <strong>Movie Easter Egg Lens</strong> | Powered by 
        <a href='https://www.themoviedb.org/' target='_blank'>TMDb</a>, 
        <a href='https://ai.google.dev/' target='_blank'>Google Gemini</a>, 
        <a href='https://render.com/' target='_blank'>Render</a> & 
        <a href='https://streamlit.io/' target='_blank'>Streamlit</a>
    </p>
    <p>Made with ❤️ for movie enthusiasts</p>
    <p>by <strong>Sachin Prabhu</strong></p>
    <p>🔗 <a href='https://github.com/sachinprabhu007/MovieEasterEggLens' target='_blank'>View on GitHub</a></p>
</div>
""", unsafe_allow_html=True)
