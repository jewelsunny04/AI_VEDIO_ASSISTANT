"""
🎬 ReelMind — AI Video Assistant
A warm, human-feeling Streamlit front end for main.py's run_pipeline().
"""

import time
import streamlit as st
from main import run_pipeline
from core.rag_engine import ask_question

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="ReelMind · AI Video Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# THEME / CSS
# Palette: deep ink background, warm amber + coral + teal accents.
# Fonts: Fraunces (display, warm serif) + Inter (body, clean sans)
# ----------------------------------------------------------------------
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,650;1,9..144,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
:root{
    --ink:#14131c;
    --panel:#1d1c29;
    --panel-2:#242236;
    --line:rgba(244,235,221,0.10);
    --cream:#f4ebdd;
    --muted:#a79fc0;
    --amber:#f2a154;
    --coral:#ef6f6c;
    --teal:#5fc9b8;
    --violet:#9a8cf0;
}

/* base */
html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
.stApp{
    background:
        radial-gradient(circle at 12% -10%, rgba(242,161,84,0.14), transparent 45%),
        radial-gradient(circle at 90% 0%, rgba(154,140,240,0.12), transparent 40%),
        var(--ink);
    color: var(--cream);
}
h1,h2,h3,h4 { font-family:'Fraunces', serif !important; color:var(--cream) !important; letter-spacing:-0.01em;}
p, span, label, div { color: var(--cream); }
small, .muted { color: var(--muted) !important; }

/* hide default streamlit chrome bits */
#MainMenu, footer {visibility:hidden;}
header[data-testid="stHeader"]{ background: transparent; }

/* ---- Hero ---- */
.hero{
    padding: 2.4rem 2.2rem;
    border-radius: 22px;
    margin-bottom: 1.6rem;
    background: linear-gradient(120deg, rgba(242,161,84,0.18), rgba(239,111,108,0.12) 45%, rgba(154,140,240,0.14));
    border: 1px solid var(--line);
    position: relative;
    overflow: hidden;
}
.hero::after{
    content:"";
    position:absolute; right:-60px; top:-60px;
    width:220px; height:220px; border-radius:50%;
    background: radial-gradient(circle, rgba(95,201,184,0.25), transparent 70%);
}
.hero-eyebrow{
    display:inline-flex; align-items:center; gap:.5rem;
    font-size:0.78rem; letter-spacing:.14em; text-transform:uppercase;
    color: var(--amber); font-weight:600; margin-bottom:.6rem;
}
.hero h1{ font-size:2.5rem; margin:0 0 .4rem 0; font-weight:650;}
.hero p{ color:var(--muted); font-size:1.02rem; max-width:640px; margin:0;}

/* ---- Cards ---- */
.card{
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1rem;
}
.card-title{
    display:flex; align-items:center; gap:.55rem;
    font-family:'Fraunces', serif; font-size:1.15rem; font-weight:650;
    margin-bottom:.7rem; color:var(--cream);
}
.badge{
    display:inline-block; padding:.15rem .6rem; border-radius:99px;
    font-size:.72rem; font-weight:600; letter-spacing:.03em;
    margin-left:.4rem;
}
.badge-amber{ background:rgba(242,161,84,0.18); color:var(--amber); }
.badge-coral{ background:rgba(239,111,108,0.18); color:var(--coral); }
.badge-teal{ background:rgba(95,201,184,0.18); color:var(--teal); }
.badge-violet{ background:rgba(154,140,240,0.20); color:var(--violet); }

/* list items pulled from plain text blocks */
.item-row{
    display:flex; gap:.7rem; padding:.55rem 0;
    border-bottom: 1px dashed var(--line);
    align-items:flex-start;
}
.item-row:last-child{ border-bottom:none; }
.item-dot{ margin-top:.35rem; width:7px; height:7px; border-radius:50%; flex-shrink:0;}

/* transcript box */
.transcript-box{
    max-height: 420px; overflow-y:auto;
    background: var(--panel-2);
    border:1px solid var(--line);
    border-radius: 14px; padding: 1rem 1.2rem;
    font-size:.92rem; line-height:1.6; color: var(--muted);
    white-space: pre-wrap;
}

/* sidebar */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg, #17151f, #1b1826 60%, #17151f);
    border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] h2{ font-size:1.3rem; }

/* inputs */
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div, .stFileUploader{
    background: var(--panel-2) !important;
    border: 1px solid var(--line) !important;
    color: var(--cream) !important;
    border-radius: 12px !important;
}

/* buttons */
.stButton>button, .stFormSubmitButton>button{
    background: linear-gradient(120deg, var(--coral), var(--amber));
    color: #1a1420; font-weight:700; border:none;
    border-radius: 12px; padding:.6rem 1.1rem;
    transition: transform .15s ease, box-shadow .15s ease;
    box-shadow: 0 6px 18px rgba(239,111,108,0.25);
}
.stButton>button:hover, .stFormSubmitButton>button:hover{
    transform: translateY(-1px);
    box-shadow: 0 10px 22px rgba(239,111,108,0.35);
}

/* tabs */
.stTabs [data-baseweb="tab-list"]{ gap: 6px; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"]{
    background: transparent; color: var(--muted); border-radius: 10px 10px 0 0;
    padding: .5rem 1rem; font-weight:600;
}
.stTabs [aria-selected="true"]{
    color: var(--cream) !important;
    background: var(--panel) !important;
    border: 1px solid var(--line);
    border-bottom: none;
}

/* chat bubbles */
.chat-user{
    background: linear-gradient(120deg, rgba(154,140,240,0.22), rgba(95,201,184,0.14));
    border:1px solid var(--line); border-radius: 16px 16px 4px 16px;
    padding: .7rem 1rem; margin: .4rem 0; max-width: 80%; margin-left:auto;
}
.chat-bot{
    background: var(--panel-2);
    border:1px solid var(--line); border-radius: 16px 16px 16px 4px;
    padding: .7rem 1rem; margin: .4rem 0; max-width: 80%;
}

/* divider */
.soft-hr{ height:1px; background: var(--line); margin: 1.2rem 0; border:none; }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------

def render_list_card(title, icon, badge_text, badge_class, content, dot_color, empty_msg):
    """Render extractor output (string or list) as a friendly card."""
    if isinstance(content, str):
        items = [line.strip("-• ").strip() for line in content.split("\n") if line.strip()]
    elif isinstance(content, (list, tuple)):
        items = [str(i).strip() for i in content if str(i).strip()]
    else:
        items = []

    rows = ""
    if items:
        for item in items:
            rows += f'<div class="item-row"><div class="item-dot" style="background:{dot_color};"></div><div>{item}</div></div>'
    else:
        rows = f'<p class="muted" style="margin:0;">{empty_msg}</p>'

    st.markdown(f"""
    <div class="card">
        <div class="card-title">{icon} {title} <span class="badge {badge_class}">{len(items)}</span></div>
        {rows}
    </div>
    """, unsafe_allow_html=True)


def init_state():
    defaults = {
        "result": None,
        "chat_history": [],
        "processing": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# ----------------------------------------------------------------------
# SIDEBAR — INPUT PANEL
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎬 ReelMind")
    st.markdown('<p class="muted">Turn any recording into a summary, action list, and a chat partner.</p>', unsafe_allow_html=True)
    st.markdown('<hr class="soft-hr">', unsafe_allow_html=True)

    input_mode = st.radio("Source type", ["YouTube link", "Upload a file"], horizontal=False)

    source = None
    if input_mode == "YouTube link":
        source = st.text_input("Paste a YouTube URL", placeholder="https://youtube.com/watch?v=...")
    else:
        uploaded = st.file_uploader("Upload audio or video", type=["mp4", "mp3", "wav", "m4a", "mov"])
        if uploaded is not None:
            save_path = f"/tmp/{uploaded.name}"
            with open(save_path, "wb") as f:
                f.write(uploaded.getbuffer())
            source = save_path
            st.success(f"Ready: {uploaded.name}")

    language = st.selectbox("Language", ["english", "hinglish"], index=0)

    st.markdown('<hr class="soft-hr">', unsafe_allow_html=True)
    run_clicked = st.button("✨ Process video", use_container_width=True)

    st.markdown('<hr class="soft-hr">', unsafe_allow_html=True)
    st.markdown('<p class="muted" style="font-size:.8rem;">Works with meetings, lectures, podcasts, or any spoken-word video.</p>', unsafe_allow_html=True)

# ----------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🎙️ AI Video Assistant</div>
    <h1>Give your recordings a memory.</h1>
    <p>Drop in a video or a link — get a clean transcript, a human-readable summary,
    the decisions that were made, and a chat window to ask it anything afterward.</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# RUN PIPELINE
# ----------------------------------------------------------------------
if run_clicked:
    if not source:
        st.warning("Add a YouTube link or upload a file first — I need something to work with 🎞️")
    else:
        steps = [
            "Listening closely to the audio…",
            "Writing down every word…",
            "Reading between the lines for a summary…",
            "Spotting decisions and action items…",
            "Building the chat memory…",
        ]
        progress = st.progress(0, text=steps[0])
        try:
            # Lightweight progress feel; actual work happens in run_pipeline
            for i, step in enumerate(steps[:-1]):
                progress.progress(int((i / len(steps)) * 80), text=step)
                time.sleep(0.15)
            result = run_pipeline(source, language=language)
            progress.progress(100, text="Done!")
            time.sleep(0.3)
            progress.empty()
            st.session_state.result = result
            st.session_state.chat_history = []
            st.toast("Your video has been processed 🎉", icon="✅")
        except Exception as e:
            progress.empty()
            st.error(f"Something went wrong while processing: {e}")

# ----------------------------------------------------------------------
# RESULTS
# ----------------------------------------------------------------------
result = st.session_state.result

if result:
    st.markdown(f"""
    <div class="card" style="border-color: rgba(242,161,84,0.3);">
        <div class="card-title">📌 {result.get('title', 'Untitled video')}
            <span class="badge badge-amber">Title</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_overview, tab_items, tab_transcript, tab_chat = st.tabs(
        ["🗂️ Overview", "✅ Action Board", "📝 Transcript", "💬 Chat with the video"]
    )

    with tab_overview:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📋 Summary</div>
            <p style="line-height:1.7;">{result.get('summary', '')}</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            render_list_card("Key Decisions", "🔑", "Decisions", "badge-teal",
                              result.get("key_decisions", ""), "#5fc9b8",
                              "No firm decisions were spotted in this one.")
        with c2:
            render_list_card("Open Questions", "❓", "Open", "badge-violet",
                              result.get("open_questions", ""), "#9a8cf0",
                              "No dangling questions — nice and tidy!")

    with tab_items:
        render_list_card("Action Items", "✅", "To-do", "badge-coral",
                          result.get("action_items", ""), "#ef6f6c",
                          "Nothing to action here — smooth sailing.")

    with tab_transcript:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📝 Full Transcript</div>
            <div class="transcript-box">{result.get('transcript', '')}</div>
        </div>
        """, unsafe_allow_html=True)

    with tab_chat:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💬 Ask anything about this video</div>', unsafe_allow_html=True)

        for role, msg in st.session_state.chat_history:
            css_class = "chat-user" if role == "user" else "chat-bot"
            speaker = "You" if role == "user" else "🎬 Assistant"
            st.markdown(f'<div class="{css_class}"><b>{speaker}:</b> {msg}</div>', unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            col1, col2 = st.columns([5, 1])
            with col1:
                question = st.text_input("Your question", placeholder="e.g. What did we decide about the launch date?", label_visibility="collapsed")
            with col2:
                send = st.form_submit_button("Ask →", use_container_width=True)

        if send and question.strip():
            st.session_state.chat_history.append(("user", question.strip()))
            with st.spinner("Thinking it over…"):
                try:
                    answer = ask_question(result["rag_chain"], question.strip())
                except Exception as e:
                    answer = f"I hit a snag answering that: {e}"
            st.session_state.chat_history.append(("bot", answer))
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="card" style="text-align:center; padding:3rem 1.5rem;">
        <h3 style="margin-bottom:.4rem;">🎞️ Nothing processed yet</h3>
        <p class="muted">Paste a YouTube link or upload a file in the sidebar, then hit
        <b>Process video</b> to see the summary, action items, and chat show up here.</p>
    </div>
    """, unsafe_allow_html=True)