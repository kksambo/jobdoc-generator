

from pdf.generator import PDFGenerator
from datetime import datetime
import os

pdf = PDFGenerator("pdf/templates")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UTILS_DIR = os.path.join(BASE_DIR, "pdf", "templates")
CERT_DIR = os.path.join(BASE_DIR, "uploads", "certificates")
os.makedirs(CERT_DIR, exist_ok=True)


def abs_path(relative_path: str):
    path = os.path.join(UTILS_DIR, relative_path)
    return path if os.path.exists(path) else None

logo_file = abs_path("templates/logo.png")


print(logo_file)
context = {
    "full_name": "Sicelo Sambo",
    "job_title": "Junior Software Developer",

    "email": "sicelo.sambo@email.com",
    "phone": "+27 71 234 5678",
    "location": "Johannesburg, South Africa",

    "profile_summary": (
        "Motivated and detail-oriented junior software developer with a passion "
        "for building clean, user-friendly applications. Strong interest in web "
        "development, APIs, and problem-solving."
    ),

    # Experience
    "role": "Software Development Intern",
    "company_name": "Tech Solutions Pty Ltd",
    "start_date": "Jan 2024",
    "end_date": "Dec 2024",
    "responsibility_1": "Developed and maintained web applications using Java and Spring Boot",
    "responsibility_2": "Collaborated with team members to design RESTful APIs",
    "responsibility_3": "Assisted in debugging, testing, and improving system performance",

    # Education
    "qualification": "Advanced Diploma in Information Technology",
    "institution": "Tshwane University of Technology",
    "graduation_year": "2024",

    # Skills
    "skill_1": "Java",
    "skill_2": "Spring Boot",
    "skill_3": "HTML & CSS",
    "skill_4": "SQL & Databases",
}

pdf.generate(
    template_name="certificate3.html",
    output_filename="certificate3.pdf",
    # context={
    #     "certificate_title": "CERTIFICATE OF COMPLETION",
    #     "recipient_name": "Sicelo Sambo",
    #     "course_description": "Health & Safety Training",
    #     "issuing_authority": "ABC Training",
    #     "date": datetime.now().strftime("%Y-%m-%d"),
    #     "logo": "/Users/sicelo/Desktop/jinja2-prac/logo.png",
    #     "alt":"alt text",
    # }
    context=context,
)
