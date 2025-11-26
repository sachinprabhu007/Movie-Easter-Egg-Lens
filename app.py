import streamlit as st
import google.generativeai as genai
import os

# -----------------------------
# Configure Gemini API key
# -----------------------------
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error(
        "❌ GOOGLE_API_KEY not found in environment variables. "
        "Set it in Render or your system before running the app."
    )
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# -----------------------------
# Gemini model
# -----------------------------
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="""
You are a huge movie fan. Chat casually and enthusiastically about hidden Easter eggs, references, and fun details in movies. Use emojis, short sentences, and be friendly.
"""
)

# -----------------------------
# Function to query Gemini multiple times
# -----------------------------
def find_multiple_easter_eggs(movie_query, num_responses=3):
    responses = []
    for _ in range(num_responses):
        try:
            chat = model.start_chat(history=[])
            response = chat.send_message(movie_query)
            responses.append(response.text)
        except Exception as e:
            responses.append(f"❌ Error: {str(e)}")
    return responses

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Movie Easter Egg Lens", page_icon="🎬")
st.title("🎬 Movie Easter Egg Lens 🥚")
st.markdown(
    "Ask about any movie you would like to find easter eggs about, for example **Harry Potter**, **Inception**, or **Interstellar** to get multiple hidden Easter eggs and fun movie secrets! 😎"
)

# User input
movie_query = st.text_input(
    "Enter a movie or scene:",
    placeholder="e.g., 'Hidden details in Harry Potter: Quidditch scenes'"
)

num_responses = st.slider("How many Easter egg answers?", 1, 5, 3)

if st.button("🔍 Find Easter Eggs"):
    if movie_query.strip():
        st.info("🎬 Searching for hidden Easter eggs...")
        results = find_multiple_easter_eggs(movie_query, num_responses=num_responses)
        for i, res in enumerate(results, 1):
            with st.expander(f"🍿 Easter Egg {i}"):
                st.write(res)

# -----------------------------
# Example prompts
# -----------------------------
st.subheader("💡 Try these:")
examples = [
    "What hidden stuff is in the first Harry Potter movie?",
    "Inception's spinning top scene – any cool Easter eggs?",
    "Any fun secrets in Interstellar's tesseract scene?",
    "Quidditch scenes in Harry Potter – anything I missed?",
    "Dream layers in Inception – hidden details?",
    "Interstellar – subtle things Nolan put in the movie?"
]
st.write(", ".join(examples))

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🎬 <strong>Movie Easter Egg Lens</strong> | Powered by 
        <a href='https://makersuite.google.com/' target='_blank'>Gemini API</a>, 
        <a href='https://render.com/' target='_blank'>Render</a> & 
        <a href='https://streamlit.io/' target='_blank'>Streamlit</a>
    </p>
    <p>Made with ❤️ for movie enthusiasts</p>
    <p>by Sachin Prabhu</p>
    <p>🔗 <a href='https://github.com/sachinprabhu007/movie-easter-egg-lens' target='_blank'>View on GitHub</a></p>
</div>
""", unsafe_allow_html=True)
