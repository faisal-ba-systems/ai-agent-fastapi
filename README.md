# AI Automation Agent

A FastAPI-based AI agent powered by Groq (LLaMA 3.3 70B) that can read/write files, run shell commands, and fetch web pages — all from a clean web UI.

## Features

- Natural language task input via browser UI
- Agentic loop with configurable max iterations
- Built-in tools: `read_file`, `write_file`, `run_shell`, `web_fetch`
- Displays tool calls made and iteration count per run

## Setup

1. **Clone & install**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Add your GROQ_API_KEY to .env
   ```

3. **Run**
   ```bash
   python -m app.main
   ```
   Open [http://localhost:8000](http://localhost:8000)

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web UI |
| GET | `/health` | Health check |
| POST | `/run` | Run agent task |

**POST /run body:**
```json
{
  "task": "List files and write a summary to output/summary.txt",
  "max_iterations": 10
}
```

## Stack

- **FastAPI** — web server
- **Groq** — LLM inference (LLaMA 3.3 70B tool-use)
- **Pydantic** — request/response models
