import os
import textwrap
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from response_generator import call_gemini, call_deepseek
from prompts import PROMPT_GENERAL

# Load API keys
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq model
llm_versatile = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="Ilama-3.3-70b-versatile")


def split_text(text, max_length=2000):
    """Splits text into smaller chunks of approximately `max_length` tokens."""
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_length:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def summarize_chunk(chunk, model="gemini-1.5-flash"):
    """Summarizes an individual text chunk while preserving medical details."""

    summary_prompt = f"""
    Given the following medical analysis, extract key insights while **preserving all critical details**:

    🔹 **Medical Observations**:
      - Include vitals (BP, HR, SpO2, temp, etc.) and lab results with abnormal values highlighted ant they should be shown pointwise for understandablity.

    🔹 **Possible Diagnoses or Conditions**:
      - List all mentioned or inferred medical conditions.

    🔹 **Recommended Treatments**:
      - Mention prescribed medications, therapies, procedures, or interventions.

    🔹 **Home Remedies & Nutraceuticals**:
      - If available, list any home remedies or natural supplements suggested.
      - For each, mention the **intended benefit** (e.g., "reduces inflammation", "improves digestion").

    🔹 **Warnings or Critical Alerts**:
      - Highlight anything urgent or risky (e.g., abnormal readings, life-threatening symptoms).

    ⚠️ Ensure full medical accuracy. Do NOT skip, simplify, or generalize any clinical observation.

    === Medical Report Chunk ===
    {chunk}
    """

    if model == "gemini-1.5-flash":
        return call_gemini(summary_prompt)
    elif model == "deepseek":
        return call_deepseek(summary_prompt)
    else:
        return "⚠️ No valid summarization model selected."


def merge_responses(summaries):
    """Merges summarized responses into a structured, user-friendly final report."""

    combined_summary = "\n\n".join(summaries)

    final_prompt = f"""
    The following is a merged summary from multiple AI-generated medical chunks:

    {combined_summary}

    ---

    Based on this, generate a **final structured report** that is:
    - Easy to understand (for a general audience)
    - Concise but medically informative
    - Actionable (clear steps for remedies, lifestyle, medications if any)
    - Reassuring yet realistic (mention if a doctor visit is essential)
    - Include vitals (BP, HR, SpO2, temp, etc.) and lab results with abnormal values highlighted ant they should be shown pointwise for understandablity
    - Recommended Actions should be Clearly split into: (iii-a) **Home Remedies 🌿** and (iii-b) **Nutraceutical Advice 💊** in different paragraphs.
    - All the subpoints should strictly and absolutely have " - " as the bulletpointsumbol in the output generated and no other symbols.
      
    🔖 **Format Required:**

    1️⃣ **Diagnosis**  
    - Mention all possible or confirmed medical conditions in plain language.

    2️⃣ **Key Symptoms**  
    - Summarize the major symptoms described in the report.

    3️⃣ **Recommended Actions** 
    Clearly split into:
    (iii-a) **Home Remedies 🌿**  
    - List any natural or household suggestions.  
    - For each, add its **intended benefit** (e.g., "soothes throat", "boosts immunity").

    (iii-b) **Nutraceutical Advice 💊**  
    - Mention vitamins, supplements, herbs, or over-the-counter aids.  
    - State each one's **intended benefit** (e.g., "improves digestion", "reduces inflammation").

    4️⃣ **Doctor's Tip 🩺**  
    - Add a short wellness or precaution tip that feels personal and professional.

    ✅ Ensure:
    - No medical info is skipped or hallucinated
    - All advice remains aligned with the provided content
    - Tone is respectful, reassuring, and informative
    - All the subpoints should strictly and absolutely have " - " as the bulletpointsumbol in the output generated and no other symbols.
    """

    try:
        response = llm_versatile.invoke(final_prompt)
        return response.content.strip() if response else "⚠️ Unable to generate a final response."
    except Exception as e:
        return f"⚠️ Error while merging responses: {str(e)}"


if __name__ == "__main__":
    # Split long medical report into chunks
    report_chunks = split_text(PROMPT_GENERAL, max_length=2000)

    # Summarize each chunk separately
    summarized_chunks = []
    for chunk in report_chunks:
        try:
            summary = summarize_chunk(chunk, model="gemini-1.5-flash")
            summarized_chunks.append(summary)
        except Exception as e:
            print(f"⚠️ Error summarizing chunk: {e}")

    # Merge summaries into final response
    final_response = merge_responses(summarized_chunks)

    print("\n=== Final Merged Response ===\n", final_response)
