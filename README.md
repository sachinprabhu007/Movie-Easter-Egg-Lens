# 🎬 Movie Easter Egg Lens 🔍

Discover hidden Easter eggs, references, and fun secrets in your favorite movies! Ask about any movie or scene and get **5–10 unique Easter eggs** generated in a human-like, enthusiastic style with emojis. Optional posters are fetched from TMDb for visual context.

---

## 🌟 Features

- Ask about any movie or scene (e.g., *Harry Potter*, *Inception*)  
- Get 5–10 unique Easter eggs in a single response  
- Human-like, casual, emoji-rich responses  
- Optional TMDb poster displayed with Easter eggs  
- Chat history maintained (newest first)  
- Black background with film strips for immersive movie vibe  
- Clear Chat option to reset history  

---

## 🏗️ Architecture

The app combines **Streamlit**, **Google Gemini**, and **TMDb API**:

1️⃣ Frontend (UI Layer — Streamlit) Frontend (UI Layer — Streamlit)

Header & Instructions

Title: 🔍 Movie Easter Egg Lens

Instructions: “Ask about any movie you would like to find Easter eggs…”

Examples Section

Shows 6 example queries (Harry Potter, Inception, Interstellar)

Input Area

Textbox: user enters a movie or scene

Buttons:

🔍 Find Easter Eggs → triggers TMDb + Gemini logic

🗑️ Clear Chat → resets session state

Chat Display (history)

Shows entries in newest-first order

Labels:

You: for user

Easter Egg 🥚: for Gemini response

Optional poster image from TMDb per entry

Footer

Movie enthusiast branding

Links: TMDb, Google Gemini, Render, Streamlit, GitHub

2️⃣ Backend / Logic Layer

TMDb API integration

Searches for movie using canonical title (if extracted) or raw input

Returns poster URL (optional)

Handles multiple results but picks the first match (you could enhance for old/new versions as discussed)

Gemini API integration

Main model (egg_model): generates 5–10 Easter eggs per query

Helper model (title_extract_model): extracts canonical movie title from user input

Ensures:

Single Gemini call for Easter eggs per query

Human-like, enthusiastic responses with emojis

Bulleted/numbered output, concise

Session State

Stores chat_history with:

user: user prompt

assistant: Gemini response

poster: TMDb image URL

title_hint: canonical title extracted

3️⃣ Flow of a Query

User enters a movie or scene → clicks 🔍

Canonical title extraction via Gemini (title_extract_model)

TMDb API call → fetch poster for canonical title or raw input

Easter eggs generation via Gemini (egg_model)

Response + poster inserted at top of chat history

UI displays:

Poster (if available)

Gemini-generated Easter eggs

Previous queries remain, newest first

4️⃣ Deployment & Environment

Render.com hosting

Environment variables:

GOOGLE_API_KEY → Gemini

TMDB_API_KEY → TMDb

MovieEasterEggLens/
│
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── LICENSE                 # License file
├── .gitignore              # Git ignore file

**Components:**

1. **Streamlit UI**
   - Input box for user queries  
   - Buttons: 🔍 Find Easter Eggs & 🗑️ Clear Chat  
   - Chat display: user input + Easter Egg 🥚 response + poster  
   - Footer with links  

2. **Google Gemini API**
   - `title_extract_model` → Extracts canonical movie titles  
   - `egg_model` → Generates 5–10 Easter eggs in human style  

3. **TMDb API**
   - Fetches posters/backdrops for visual context  
   - Optional; works if a valid TMDb API key is provided  

4. **Session State**
   - Stores chat history (newest queries appear on top)  

---

## 💡 Try These Examples

- What hidden stuff is in the first Harry Potter movie?  
- Inception's spinning top scene – any cool Easter eggs?  
- Any fun secrets in Interstellar's tesseract scene?  
- Quidditch scenes in Harry Potter – anything I missed?  
- Dream layers in Inception – hidden details?  
- Interstellar – subtle things Nolan put in the movie?  

---

## 🛠️ Installation

1. Clone the repository:

git clone https://github.com/sachinprabhu007/MovieEasterEggLens.git
cd MovieEasterEggLens

Install dependencies:

pip install -r requirements.txt


Set environment variables:

export GOOGLE_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"
export TMDB_API_KEY="YOUR_TMDB_API_KEY"  # Optional for posters


🔑 API Keys
TMDb API

Sign up: https://www.themoviedb.org/signup

Apply for API key: Settings → API

Documentation: Search Movie API

Google Gemini

Get free API key: https://makersuite.google.com/app/apikey

Documentation: Google Generative AI

💻 Usage

Run the app:

streamlit run app.py


Type your query (e.g., "Hidden details in Harry Potter: Quidditch scenes")

Click 🔍 Find Easter Eggs

View the Easter Egg 🥚 responses and poster image

Use 🗑️ Clear Chat to reset history

🏗️ Deployment on Render

Build Command: pip install -r requirements.txt

Start Command: streamlit run app.py --server.port $PORT --server.enableCORS false

Environment Variables: GOOGLE_API_KEY and TMDB_API_KEY

Optional: Enable Auto-Deploy from GitHub

🖼️ Screenshots


User query with Gemini-generated Easter eggs and TMDb poster


Newest responses appear on top, posters optional

📦 Dependencies

- streamlit
- requests
- google-generativeai

📜 License

Copyright (c) 2025 Sachin Prabhu

This software is licensed for educational and personal use only.

You may not use, copy, modify, distribute, or sell this software or any part of it without explicit written permission from the copyright holder.

Any commercial use or other unauthorized use is strictly prohibited.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
