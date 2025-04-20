from flask import Flask, request, jsonify
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load API Key
load_dotenv()
api_key = "AIzaSyBSe66nRNUzSakt7PcVXaLqhFj2LRL8jws"
genai.configure(api_key=api_key)

app = Flask(__name__)
CORS(app)  # Allow frontend to call API if served separately

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if text.strip():
            print("✅ Extracted text using pdfplumber.")
            return text.strip()
    except Exception as e:
        print("❌ pdfplumber failed:", e)

    try:
        images = convert_from_path(pdf_path)
        for image in images:
            text += pytesseract.image_to_string(image) + "\n"
        print("✅ Extracted text using OCR.")
    except Exception as e:
        print("❌ OCR failed:", e)

    return text.strip() if text.strip() else "Error: No text extracted."

def analyze_resume(resume_text, job_description=None):
    if not resume_text:
        return jsonify({"success": False, "error": "Resume text is empty."})

    model = genai.GenerativeModel("gemini-1.5-flash")

    base_prompt = f"""
    You are an HR expert analyzing resumes. Please provide feedback on the resume below.

    Resume:
    {resume_text}
    """

    if job_description:
        base_prompt += f"\n\nCompare this with the following job description:\n{job_description}"

    try:
        response = model.generate_content(base_prompt)
        print("🔍 Gemini API response received.")
        return jsonify({"success": True, "analysis": response.text.strip()})
    except Exception as e:
        print("❌ Gemini Error:", e)
        return jsonify({"success": False, "error": "Gemini API error occurred."})

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('resume')
    job_description = request.form.get('jobDescription')

    if not file:
        return jsonify({"success": False, "error": "Resume file is required."}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    print(f"📄 Resume uploaded: {file.filename}")

    resume_text = extract_text_from_pdf(file_path)
    print("📄 Extracted Resume Text:\n", resume_text[:500])  # Show first 500 chars
    return analyze_resume(resume_text, job_description)

if __name__ == '__main__':
    app.run(debug=True)
