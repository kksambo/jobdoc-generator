import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_KEY")
)

def generate_cover_letter(context: dict) -> str:
    prompt = f"""
Write a professional cover letter using the following information.

Applicant Details:
Full Name: {context['full_name']}
Job Title: {context['job_title']}
Email: {context['email']}
Phone: {context['phone']}
Location: {context['location']}

Profile Summary:
{context['profile_summary']}

Experience:
Role: {context['role']}
Company: {context['company_name']}
Period: {context['start_date']} to {context['end_date']}

Skills:
{", ".join(context['skills'])}

Instructions:
- Professional and confident tone
- Clear and concise
- Start with "Dear Hiring Manager,"
- End with a professional closing and full name
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # FAST & FREE
        messages=[
            {"role": "system", "content": "You are a professional career assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=600
    )

    return completion.choices[0].message.content


# -----------------------------
# TEST RUN
# -----------------------------
if __name__ == "__main__":
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
        "role": "Software Development Intern",
        "company_name": "Tech Solutions Pty Ltd",
        "start_date": "Jan 2024",
        "end_date": "Dec 2024",
        "skills": [
            "Java",
            "Spring Boot",
            "HTML & CSS",
            "SQL & Databases"
        ]
    }

    print("\n📝 GENERATED COVER LETTER (Groq)\n")
    letter = generate_cover_letter(context)
    print(letter)
