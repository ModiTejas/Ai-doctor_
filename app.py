import streamlit as st
from response_generator import process_with_all_models
from report_extractor import process_uploaded_files

# Set default session state for greeting
if "hide_greeting" not in st.session_state:
    st.session_state.hide_greeting = False

# App config
st.set_page_config(page_title="AI Doctor Assistant 🏥", layout="wide")
st.title("🤖 AI-Powered Doctor Assistant")

# Sidebar for inputs
st.sidebar.header("📝 Patient Details")
name = st.sidebar.text_input("👤 Name", placeholder="Enter your full name")
age = st.sidebar.number_input("🎂 Age", min_value=1, max_value=120, step=1)
symptoms = st.sidebar.text_area("💬 Describe Your Symptoms", placeholder="E.g., fever, cough, body ache")

# File uploader
st.sidebar.header("📂 Upload Medical Reports (Optional)")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDF or Images (ECG, Blood Report, etc.)",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# Extract content
report_content = process_uploaded_files(uploaded_files)

# Greeting
if (not symptoms.strip() and not report_content.strip()) and not st.session_state.hide_greeting:
    st.write("Hello! 😊 Enter your symptoms, age, and upload reports (if needed) to receive medically accurate and **calm, friendly advice.**")

# Warning
st.warning("""⚠️ **Important Notice**: This AI assistant provides general health information only. 
It is not a substitute for professional medical advice, diagnosis, or treatment.
Always seek the advice of your physician with any medical concerns.""")

# Theme settings
theme = st.get_option("theme.base")
bg_color = "rgba(255, 255, 255, 0.85)" if theme == "light" else "rgba(20, 20, 20, 0.6)"
text_color = "#222" if theme == "light" else "#eee"
border_color = "rgba(200, 200, 200, 0.4)" if theme == "light" else "rgba(255, 255, 255, 0.1)"

# Main button
if st.sidebar.button("🩺 Get AI Medical Advice"):
    if not symptoms.strip() and not report_content.strip():
        st.warning("⚠️ Please enter your symptoms or upload a medical report before proceeding.")
    else:
        st.session_state.hide_greeting = True
        with st.spinner("🔍 Analyzing your symptoms and generating advice..."):
            prompt = f"""
            Patient Name: {name if name else 'Anonymous'}
            Age: {age if age else 'Not Provided'}
            Symptoms: {symptoms if symptoms else 'Not Provided'}
            Medical Report Details: {report_content if report_content else 'No reports uploaded.'}

            Based on this, provide a medically accurate and calm response. Include:
            - Home remedies
            - Nutraceutical advice
            - Dietary tips
            - If necessary, a doctor referral
            """

            final_response = process_with_all_models(prompt)

        # Clean markdown
        import re
        def clean_markdown(text):
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            text = re.sub(r'\*(.*?)\*', r'\1', text)
            text = re.sub(r'#+\s*(.*?)\n', r'\1\n', text)
            return text.strip()

        cleaned_response = clean_markdown(final_response)

        st.markdown("""
            <style>
                .frosted-box {
                    background: rgba(255, 255, 255, 0.08);
                    padding: 24px;
                    border-radius: 20px;
                    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
                    backdrop-filter: blur(12px);
                    -webkit-backdrop-filter: blur(12px);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    margin-bottom: 30px;
                    color: var(--text-color);
                }
                .frosted-box h3 {
                    color: var(--primary-color);
                    margin-top: 0;
                }
                .frosted-box strong {
                    color: var(--primary-color);
                }
            </style>

            <div class="frosted-box">
                <h3>💡 AI Doctor's Advice</h3>
                <div style="font-size: 16px; line-height: 1.6;">
                    """ + cleaned_response.replace("\n", "<br>") + """
                    <br><br>
                    <strong>💖 Doctor’s Health Tips</strong><br><br>
                    🌞 Morning Tip: Start your day with lukewarm lemon water to boost immunity & digestion. 🍋<br>
                    🍽️ Nutrition Tip: Eat colorful vegetables for essential vitamins and better gut health. 🥕🥬<br>
                    🏋️‍♂️ Exercise Tip: A daily 20-minute walk improves heart health & reduces stress. 🚶‍♀️<br>
                    😴 Sleep Tip: Avoid screens before bedtime to ensure deep, restful sleep. 😴💤<br>
                    💖 Mental Health Tip: Practice slow, deep breathing to calm anxiety and improve focus. 🌿<br>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("🤖 **Powered by LLaMA, Gemini & DeepSeek AI** | Created with ❤️ by AI Health Experts")
