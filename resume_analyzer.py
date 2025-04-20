from flask import Flask, request, jsonify
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS
from typing import Dict, Union, Optional

# Load environment variables and configure API
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyBSe66nRNUzSakt7PcVXaLqhFj2LRL8jws")
genai.configure(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Constants
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file using multiple methods.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text or error message
    """
    text = ""
    
    # Try pdfplumber first
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(
                page.extract_text() or "" 
                for page in pdf.pages
            ).strip()
            
        if text:
            print("✅ Extracted text using pdfplumber")
            return text
    except Exception as e:
        print("❌ pdfplumber failed:", e)
    
    # Fall back to OCR if pdfplumber fails
    try:
        images = convert_from_path(pdf_path)
        text = "\n".join(
            pytesseract.image_to_string(image) 
            for image in images
        ).strip()
        print("✅ Extracted text using OCR")
        return text
    except Exception as e:
        print("❌ OCR failed:", e)
    
    return "Error: No text extracted."

def analyze_resume(resume_text: str, job_description: Optional[str] = None) -> Dict[str, Union[bool, str, int]]:
    """
    Analyze resume text using AI and return structured feedback.
    
    Args:
        resume_text (str): Text extracted from resume
        job_description (str, optional): Job description for comparison
        
    Returns:
        dict: Analysis results including score and feedback
    """
    # Validate input
    if not resume_text:
        return {"success": False, "error": "Resume text is empty."}
    
    if resume_text == "Error: No text extracted.":
        return {
            "success": False, 
            "error": "Could not extract text from the PDF. Please ensure the PDF contains readable text."
        }

    # Prepare AI prompt with stricter scoring criteria
    model = genai.GenerativeModel("gemini-1.5-flash")
    base_prompt = f"""
    You are an expert HR professional and resume evaluator. Analyze the resume below using these strict scoring criteria:

    FORMAT AND PRESENTATION (20 points):
    - Professional layout and consistent formatting (5 points)
    - Clear section headings and organization (5 points)
    - Proper use of bullet points and white space (5 points)
    - No spelling/grammar errors (5 points)

    CONTENT QUALITY (30 points):
    - Quantifiable achievements with specific metrics (10 points)
    - Clear and concise descriptions (5 points)
    - Relevant keywords and industry terminology (5 points)
    - Strong action verbs and impactful language (5 points)
    - Proper length and detail level (5 points)

    EXPERIENCE AND ACHIEVEMENTS (30 points):
    - Relevant work experience for the field (10 points)
    - Demonstrated progression and growth (5 points)
    - Project details with measurable outcomes (10 points)
    - Leadership or initiative shown (5 points)

    SKILLS AND QUALIFICATIONS (20 points):
    - Required technical skills present (8 points)
    - Relevant certifications/education (5 points)
    - Soft skills demonstration (4 points)
    - Up-to-date technology/tools (3 points)

    Deduct points for:
    - Missing or incomplete information (-5 each)
    - Irrelevant information (-3 each)
    - Poor formatting or organization (-3 each)
    - Lack of specificity in achievements (-3 each)
    - Generic descriptions (-2 each)

    Your response should be structured EXACTLY as follows:
    SCORE: [numerical score]

    ANALYSIS:

    STRENGTHS:
    [List key strengths with bullet points]

    WEAKNESSES:
    [List areas for improvement with bullet points]

    RECOMMENDATIONS:
    [List specific recommendations with bullet points]

    Resume:
    {resume_text}
    """

    if job_description:
        base_prompt += f"""
        
        Compare with Job Description:
        Consider how well the resume matches these job requirements and adjust scoring accordingly:
        {job_description}

        Additional scoring criteria for job match:
        - Deduct 10 points if critical required skills are missing
        - Deduct 5 points if experience level doesn't match
        - Deduct 3 points for each missing preferred qualification
        """

    try:
        # Generate and parse AI response
        response = model.generate_content(base_prompt)
        response_text = response.text.strip()
        
        try:
            # Extract score
            lines = response_text.split('\n')
            score_line = next(line for line in lines if line.strip().startswith('SCORE:'))
            score = int(score_line.replace('SCORE:', '').strip())
            
            # Extract analysis
            analysis_start = next(
                (i for i, line in enumerate(lines) if line.strip().startswith('ANALYSIS:')), 
                1
            )
            analysis = '\n'.join(lines[analysis_start + 1:]).strip()
            
            if not analysis:
                raise ValueError("No analysis text found")
                
            return {
                "success": True,
                "score": score,
                "analysis": analysis
            }
            
        except (ValueError, IndexError) as e:
            print("⚠️ Error parsing AI response:", e)
            print("Raw response:", response_text)
            return {
                "success": False,
                "error": "Failed to parse analysis results. Please try again."
            }
            
    except Exception as e:
        print("❌ Gemini Error:", str(e))
        return {
            "success": False,
            "error": "Failed to analyze resume. Please try again or contact support if the issue persists."
        }

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle resume analysis request."""
    file_path = None
    
    try:
        # Validate request
        file = request.files.get('resume')
        if not file:
            return jsonify({"success": False, "error": "Resume file is required."}), 400
            
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"success": False, "error": "Only PDF files are supported."}), 400

        # Save and process file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        print(f"📄 Resume uploaded: {file.filename}")

        # Extract and analyze text
        resume_text = extract_text_from_pdf(file_path)
        if not resume_text or resume_text == "Error: No text extracted.":
            return jsonify({
                "success": False,
                "error": "Could not extract text from the PDF. Please ensure the file contains readable text."
            }), 400

        job_description = request.form.get('jobDescription')
        return jsonify(analyze_resume(resume_text, job_description))

    except Exception as e:
        print("❌ Server Error:", str(e))
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500
        
    finally:
        # Clean up uploaded file
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Warning: Failed to remove temporary file {file_path}: {e}")

if __name__ == '__main__':
    app.run(debug=True)
