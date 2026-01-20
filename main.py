

from pdf.generator import PDFGenerator
from datetime import datetime
import os

pdf = PDFGenerator("pdf/cover-letter-templates")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UTILS_DIR = os.path.join(BASE_DIR, "pdf", "cv-templates")
CERT_DIR = os.path.join(BASE_DIR, "uploads", "certificates")
os.makedirs(CERT_DIR, exist_ok=True)


def abs_path(relative_path: str):
    path = os.path.join(UTILS_DIR, relative_path)
    return path if os.path.exists(path) else None

logo_file = abs_path("cv-templates/logo.png")


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
    "skills": ["Java","Spring Boot","HTML & CSS","SQL & Databases"],

    "duties": [
    "Generated, produced and maintained 42 end-to-end marketing and PR projects of which three became viral stunts. Completed all the projects within approved budget, timescale, and expected quality.",
    "Managed, led and coordinated various teams of up to 70 people to perform marketing programs. This included collaboration both with internal and external teams.",
    "Solved internal financial business challenges by reducing projects' costs by 25% while maintaining quality, thus achieving remarkable ROI.",
    "Created, organized and implemented the company’s employee training program which helped up-to-date educational book reading practices, improving professional skills and workflow."
]
}


cover_letter_context = {
    # Personal Info
    "full_name": "Sicelo Sambo",
    "job_title": "Junior Software Developer",
    "email": "sicelo.sambo@email.com",
    "phone": "+27 71 234 5678",
    "location": "Johannesburg, South Africa",

    # Recipient Info
    "recipient_name": "Hiring Manager",
    "recipient_company": "Tech Innovations Ltd",
    "recipient_position": "Software Developer",
    "date": "17 January 2026",

    # Letter Content
    "letter_body": (
        "Dear {{ recipient_name }},\n\n"
        "I am excited to apply for the {{ recipient_position }} position at {{ recipient_company }}. "
        "With my experience as a Software Development Intern at Tech Solutions Pty Ltd, I have developed and maintained web applications using Java and Spring Boot, collaborated with team members to design RESTful APIs, and contributed to debugging, testing, and optimizing system performance.\n\n"
        "I hold an Advanced Diploma in Information Technology from Tshwane University of Technology and have honed skills in Java, Spring Boot, HTML & CSS, and SQL & Databases. I am confident that my strong problem-solving abilities and passion for building clean, user-friendly applications make me a strong fit for your team.\n\n"
        "I would welcome the opportunity to discuss how my skills and experiences align with the goals of {{ recipient_company }} and how I can contribute to your ongoing projects.\n\n"
        "Thank you for your time and consideration."
    ),

    # Experience (Optional: included if you want to list achievements inside letter)
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
    "skills": ["Java", "Spring Boot", "HTML & CSS", "SQL & Databases"],

    # Duties / Achievements (Optional)
    "duties": [
        "Generated, produced and maintained 42 end-to-end marketing and PR projects of which three became viral stunts, completing all within budget and timescale.",
        "Managed and coordinated teams of up to 70 people to perform marketing programs, collaborating with internal and external teams.",
        "Reduced project costs by 25% while maintaining quality, achieving remarkable ROI.",
        "Created and implemented an employee training program that improved professional skills and workflow."
    ]
}


pdf.generate(
    template_name="simple.html",
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
    context=cover_letter_context,
)
