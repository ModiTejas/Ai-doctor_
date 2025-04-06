import PyPDF2
import requests

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        return text.strip() if text else "No readable text found in the PDF."
    except Exception:
        return "Error reading PDF."

def extract_text_from_image(image_file):
    try:
        url = 'https://api.ocr.space/parse/image'
        payload = {
            'isOverlayRequired': False,
            'apikey': 'helloworld',  # Free test key from OCR.Space
            'language': 'eng',
        }
        response = requests.post(url, files={'filename': image_file}, data=payload)
        result = response.json()
        return result['ParsedResults'][0]['ParsedText'].strip() if 'ParsedResults' in result else "OCR Failed"
    except Exception as e:
        return f"Error using OCR API: {str(e)}"

def process_uploaded_files(files):
    report_texts = []
    for file in files:
        if file.type == "application/pdf":
            report_texts.append(extract_text_from_pdf(file))
        elif file.type.startswith("image"):
            report_texts.append(extract_text_from_image(file))
    return "\n\n".join(report_texts).strip() if report_texts else ""
