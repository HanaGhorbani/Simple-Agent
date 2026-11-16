# Basic Agent

A minimal tool-calling AI agent built with LangChain and LangGraph. It follows the ReAct loop: the model reads the task, decides whether to call a tool, the harness runs the tool, the result goes back into the history, and the loop repeats until the model answers without a tool call.

Built as the hands-on part of *AI Agents, Session 1: What is an agent?*

## Features

- Two example tools: `add` (integer addition) and `get_weather` (a stub that always returns `sunny, 22°C`)
- Prompt is read from the user at runtime
- Works with any OpenAI-compatible API (configured for Groq)
- Step cap and request timeout so the agent never hangs or loops forever

## Project structure

```
basic-agent/
├── Main.py            # builds the agent and runs it
├── tools.py           # tool definitions
├── list_models.py     # lists the models available to your API key
├── .env.example       # template for your environment variables
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a virtual environment (Python 3.10 or newer, 3.12 recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   On macOS or Linux use `source .venv/bin/activate`.

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file next to `Main.py` (copy `.env.example`) and fill it in:

   ```
   OPENAI_API_KEY=your_key_here
   OPENAI_BASE_URL=https://api.groq.com/openai/v1
   MODEL=openai/gpt-oss-20b
   ```

   You can get a free API key from [console.groq.com](https://console.groq.com). Never commit `.env`.

## Choosing a model: `list_models.py`

Model names change over time, and not every model is available to every account. If you use a name that does not exist for your key, the API returns a `404 model not found` error.

`list_models.py` prints the IDs of all models your API key can currently use, so you can copy a valid name into `MODEL` in `.env`:

```bash
python list_models.py
```

Pick a model that supports tool calling. Models for speech, audio, or safety filtering (names containing `whisper`, `orpheus`, `guard`, `safeguard`) are not suitable for this agent.

## Run

```bash
python Main.py
```

Type your prompt when asked, for example:

```
Your prompt: Use the add tool for 47832 + 91347, and tell me the weather in Paris.
```

The full message trace is printed, so you can see each tool call, each tool result, and the final answer.

## Things to try

| Prompt | Expected behavior |
|---|---|
| `Weather in Paris?` | calls `get_weather` |
| `Tell me a joke.` | no tool call |
| `What is 12+30?` | small models may answer without calling `add` |
| `Use the add tool for 47832 + 91347` | calls `add` |

## Troubleshooting

| Problem | Fix |
|---|---|
| `KeyError: 'MODEL'` | `.env` is missing, misnamed (for example `.env.txt`), or not next to `Main.py` |
| `404 model does not exist` | run `list_models.py` and set a valid `MODEL` |
| `ImportError: create_agent` | `pip install -U langchain langgraph` |
| `429` errors | rate limit; wait a few seconds and retry |
| Hangs with no error | keep `timeout` and `max_retries=0` set in `Main.py` |

## Notes

- The weather tool is a stub and does not return real weather.
- Tool-call behavior depends on the model. Some models call tools one after another, others in parallel, and small models may skip a tool for easy questions.