import os
import re
import time
import textwrap
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import google.generativeai as genai



# Load API keys
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# Initialize GROQ LLMs
llm_llama = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
llm_deepseek = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="deepseek-r1-distill-llama-70b")

# Initialize Gemini LLM
genai.configure(api_key=GENAI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.0-flash", generation_config={"temperature": 1})

# Model token limits
MODEL_TOKEN_LIMITS = {
    "llama": 8000,
    "deepseek": 7000,
    "gemini": 6000
}


# Chunk text based on estimated token size
def chunk_text(text, model="llama"):
    max_tokens = MODEL_TOKEN_LIMITS.get(model, 5000) - 500
    approx_chars = max_tokens * 4
    return textwrap.wrap(text, width=approx_chars)


# Model Call Functions
def call_llama(prompt):
    try:
        response = llm_llama.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"[LLaMA Error: {e}]"

def call_deepseek(prompt):
    try:
        response = llm_deepseek.invoke(prompt)
        content = response.content.strip()
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        return content
    except Exception as e:
        return f"[DeepSeek Error: {e}]"

def call_gemini(prompt):
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Gemini Error: {e}]"


# Unified processing: apply all 3 LLMs on each chunk
def process_with_all_models(input_text):
    chunks = chunk_text(input_text, model="llama")  # Choose highest limit for chunking
    merged_responses = []

    for idx, chunk in enumerate(chunks):
        print(f"\n🔹 Processing Chunk {idx+1}/{len(chunks)}")
        llama_output = call_llama(chunk)
        deepseek_output = call_deepseek(chunk)
        gemini_output = call_gemini(chunk)

        combined = f"""🔹 **Chunk {idx+1} Summary**  
🔸 **LLaMA**: {llama_output}  
🔸 **DeepSeek**: {deepseek_output}  
🔸 **Gemini**: {gemini_output}
"""
        merged_responses.append(combined)
        time.sleep(1)

    # Combine all summaries
    final_merge_prompt = "\n\n".join(merged_responses) + """

Now, merge the above insights into a single professional and actionable medical summary.  
Format it with:  
1️⃣ Diagnosis  
2️⃣ Key Symptoms  
3️⃣ Recommended Actions  
4️⃣ Doctor’s Tip  
Ensure it is clear, helpful, and medically sound.
"""
    return call_llama(final_merge_prompt)


