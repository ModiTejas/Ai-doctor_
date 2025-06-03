# 🩺 AI Doctor

An interactive AI-powered assistant built with [Streamlit](https://streamlit.io/) that interprets symptoms, diagnoses conditions, and generates contextual medical advice based on patient inputs and lab reports. Ideal for prototyping healthcare apps and experimenting with large language models (LLMs) in a clinical support context.

🔗 Live app: [ai-doctor-1234.streamlit.app](https://ai-doctor-1234.streamlit.app/)

---

## 📌 Description

This project takes natural language inputs from users describing their symptoms or uploading health reports, and uses a custom prompt engineering pipeline to produce reliable responses. The core logic is modular and leverages the capabilities of LLMs to simulate a clinical diagnostic tool.

All language understanding and response generation is handled programmatically without third-party API wrappers. The focus is on local control, composability, and transparency.

---

## 🧠 Interesting Techniques Used

- **[Prompt engineering](https://platform.openai.com/docs/guides/gpt)** 🧾: Dynamically assembles prompts using user input and report context to steer LLM responses.
- **LLM response merging** 🔄: Combines outputs from multiple prompt strategies to generate a more robust final answer.
- **[PDF text extraction](https://pypi.org/project/PyPDF2/)** 📄: Reads and processes report text from PDFs for symptom enrichment.
- **[Streamlit widgets](https://docs.streamlit.io/library/api-reference/widgets)** 🎛️: Leverages interactive UI components for real-time feedback loops.
- **Function-based modular structure** 🧩: Keeps logic for merging, extracting, and generating responses cleanly separated for testing and maintenance.

---

## 🧰 Notable Libraries and Technologies

- **[Streamlit](https://streamlit.io/)** – For building fast, interactive web UIs in pure Python.
- **[PyPDF2](https://pypi.org/project/PyPDF2/)** – Extracts text from uploaded PDF reports.
- **[OpenAI Python SDK](https://pypi.org/project/openai/)** – Used to send requests to OpenAI LLMs.
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** – Manages API keys and environment config securely.

---

## 🗂️ Project Structure

```
├── app.py
├── merge_llm_responses.py
├── prompts.py
├── report_extractor.py
├── response_generator.py
├── requirements.txt
├── .env.example
```

### Directory Breakdown

- `app.py` – Main Streamlit app logic. Handles user inputs, file uploads, and response display.
- `prompts.py` – Contains reusable prompt templates and message formats.
- `merge_llm_responses.py` – Merges different generated outputs for robustness.
- `report_extractor.py` – Handles PDF report parsing and symptom text cleaning.
- `response_generator.py` – Sends prompts to LLM and receives answers.
- `requirements.txt` – Lists all dependencies.
- `.env.example` – Template file to show required environment variables.

---

## 🔐 API Keys

Create a `.env` file  with the following:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## 🔽 Clone This Repo

Use the following command to clone the repository:

```bash
git clone https://github.com/ModiTejas/Ai-doctor_.git

