import streamlit as st
import google.generativeai as genai
import requests
import os

# ----------------------------------------
# Environment keys
# ----------------------------------------
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ Missing GOOGLE_API_KEY in environment variables.")
    st.stop()

if not TMDB_API_KEY:
    st.error("❌ Missing TMDB_API_KEY in environment variables.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# ----------------------------------------
# Gemini model
# ----------------------------------------
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="""
You give 5–10 fresh Easter eggs for any movie. 
Be human-like, energetic, avoid repetition, and change them each time.
Use emojis naturally. Do not give filler text.
Respond only with Easter Eggs.
"""
)

# ----------------------------------------
# TMDb Search Function
# ----------------------------------------
def search_movie_tmdb(query):
    url = f"https://api.themoviedb.org/3/search/movie?query={query}&api_key={TMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if not data["results"]:
        return None

    movie = data["results"][0]  # take best match

    poster_path = movie.get("poster_path")
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

    return {
        "title": movie.get("title"),
        "id": movie.get("id"),
        "poster": poster_url
    }

# ----------------------------------------
# Get Easter Eggs
# ----------------------------------------
def find_easter_eggs(movie_query):
    try:
        chat = model.start_chat(history=[])
        response = chat.send_message(movie_query)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ----------------------------------------
# Streamlit UI
# ----------------------------------------
st.set_page_config(page_title="Movie Easter Egg Lens", page_icon="🎬")
st.title("🎬 Movie Easter Egg Lens 🔍")

st.markdown(
    "Ask about any movie you would like to find Easter eggs about — e.g., **Harry Potter**, **Inception**, **Interstellar** — and I'll pull hidden secrets, fun details, and also show the **movie poster** if it exists! 🎥✨"
)

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------------------
# User Input
# ----------------------------------------
movie_query = st.text_input("Enter a movie name:")

if st.button("🔍 Find Easter Eggs"):
    if movie_query.strip():

        # Check movie in TMDb
        movie_data = search_movie_tmdb(movie_query)

        if movie_data is None:
            st.error("❌ Movie not found on TMDb. Please check the name and try again.")
        else:
            # Show poster FIRST
            if movie_data["poster"]:
                st.image(movie_data["poster"], width=300, caption=movie_data["title"])

            # Get Easter Eggs
            st.info("🥚 Finding hidden Easter eggs...")
            easter_eggs = find_easter_eggs(movie_data["title"])

            # Save chat
            st.session_state.chat_history.append(
                (movie_query, easter_eggs, movie_data["poster"])
            )

# Clear chat
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []

# ----------------------------------------
# Chat History (latest first)
# ----------------------------------------
for human, bot, img in reversed(st.session_state.chat_history):

    st.markdown(f"**You:** {human}")

    if img:
        st.image(img, width=250)

    st.markdown(f"**Easter Egg 🥚:** {bot}")
    st.markdown("---")

# ----------------------------------------
# Example prompts
# ----------------------------------------
st.subheader("💡 Try these:")
examples = [
    "Harry Potter secrets",
    "Inception hidden details",
    "Interstellar easter eggs",
    "Avatar movie hidden references",
    "Dark Knight fun details"
]

for ex in examples:
    st.markdown(f"- {ex}")

# ----------------------------------------
# Footer
# ----------------------------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🎬 <strong>Movie Easter Egg Lens</strong> | Powered by 
        <a href='https://www.themoviedb.org/' target='_blank'>TMDb</a>, 
        <a href='https://ai.google.dev/' target='_blank'>Gemini</a>, 
        <a href='https://render.com/' target='_blank'>Render</a> & 
        <a href='https://streamlit.io/' target='_blank'>Streamlit</a>
    </p>
    <p>Made with ❤️ by Sachin Prabhu</p>
</div>
""", unsafe_allow_html=True)
