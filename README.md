# 🎬 ReelMind — AI Video Assistant

Turn any recording — a YouTube video, a meeting, a lecture, a podcast — into a clean
transcript, a human-readable summary, a list of action items and decisions, and a
chat window you can ask follow-up questions in.

---

## ✨ Features

- 🎧 **Flexible input** — process a YouTube URL or a local audio/video file
- 📝 **Transcription** — full transcript generation, with English or Hinglish support
- 📋 **Summarization** — a short, readable summary plus an auto-generated title
- ✅ **Action items** — what needs to get done, pulled straight from the conversation
- 🔑 **Key decisions** — what was actually agreed on
- ❓ **Open questions** — what's still unresolved
- 💬 **Chat with your video** — a RAG-powered Q&A interface over the transcript
- 🎨 **Streamlit UI** — a warm, colorful front end (`app.py`) on top of the core pipeline

---

## 🗂️ Project Structure

```
.
├── app.py                     # Streamlit UI (front end)
├── main.py                    # CLI entry point / pipeline orchestration
├── core/
│   ├── transcriber.py         # transcribe_all()
│   ├── summariser.py          # summarize(), generate_title()
│   ├── extractor.py           # extract_action_items(), extract_key_decisions(), extract_questions()
│   └── rag_engine.py          # build_rag_chain(), ask_question()
├── utils/
│   └── audio_processor.py     # process_input()
├── .env                       # API keys / secrets (not committed)
└── requirements.txt
```

---

## ⚙️ Requirements

- Python 3.9+
- An `.env` file with whatever API keys your `core/` modules rely on (e.g. an LLM
  provider key, transcription service key, etc.)

Install dependencies:

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet, at minimum you'll need:

```bash
pip install streamlit python-dotenv
```

plus whatever transcription / LLM / vector-store libraries your `core` and `utils`
modules use under the hood.

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
# Example — replace with whatever your core modules actually need
OPENAI_API_KEY=your_key_here
```

`main.py` loads this automatically via `load_dotenv()`.

---

## 🚀 Usage

### Option 1 — Streamlit UI (recommended)

```bash
streamlit run app.py
```

Then in the browser:
1. Paste a YouTube link, or upload an audio/video file, in the sidebar
2. Pick a language (`english` or `hinglish`)
3. Click **Process video**
4. Browse the **Overview**, **Action Board**, and **Transcript** tabs
5. Head to **Chat with the video** to ask follow-up questions

### Option 2 — Command line

```bash
python main.py
```

You'll be prompted for:
```
Enter YouTube URL or local file path: <your input>
Language (english/hinglish): english
```

The script prints the title, summary, action items, decisions, and open questions,
then drops you into an interactive chat loop:

```
💬 Chat with your meeting (type 'exit' to quit)

You: What did we decide about the launch date?
🤖 Assistant: ...
```

---

## 🧠 How It Works

1. **`process_input(source)`** — accepts a YouTube URL or local file path and
   splits it into audio chunks
2. **`transcribe_all(chunks, language)`** — transcribes each chunk and stitches
   together the full transcript
3. **`generate_title(transcript)`** / **`summarize(transcript)`** — produce a
   title and summary from the transcript
4. **`extract_action_items` / `extract_key_decisions` / `extract_questions`** —
   pull structured insights out of the raw transcript
5. **`build_rag_chain(transcript)`** — indexes the transcript for retrieval
6. **`ask_question(rag_chain, question)`** — answers follow-up questions using
   the indexed transcript

---

## 🛠️ Troubleshooting

- **Nothing happens after clicking "Process video"** — check the terminal running
  Streamlit for the actual error; long videos can take a while to transcribe.
- **File upload fails silently** — confirm `process_input()` accepts a plain
  local file path (the UI saves uploads to a temp path before passing them in).
- **Chat answers seem off** — try re-processing the video; the RAG chain is
  rebuilt fresh each time `run_pipeline()` runs.

---

## 📌 Roadmap Ideas

- [ ] Support for multiple languages beyond English/Hinglish
- [ ] Export summary + action items as PDF or Word doc
- [ ] Persist processed videos so you don't have to reprocess on refresh
- [ ] Multi-video library / history view

---

## 📄 License

Add your license of choice here (MIT, Apache 2.0, etc.).