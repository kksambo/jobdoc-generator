from fastapi import FastAPI, Body, Depends, HTTPException, Header, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os,shutil
import uuid
import uvicorn
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from groq import Groq
from pdf.generator import PDFGenerator
import requests

from typing import List




# =========================
# Load environment
# =========================
load_dotenv()

# =========================
# FastAPI instance
# =========================
app = FastAPI(title="CV & Cover Letter Generator API")

# =========================
# CORS (for React frontend)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads", "documents")
os.makedirs(UPLOAD_DIR, exist_ok=True)
# =========================
# Database setup
# =========================
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# JWT settings
# =========================
SECRET_KEY = "supersecretkey"  # replace in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# =========================
# Base directories for PDFs
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CV_TEMPLATES_DIR = os.path.join(BASE_DIR, "pdf", "cv-templates")
CV_OUTPUT_DIR = os.path.join(BASE_DIR, "uploads", "certificates")

COVER_LETTER_TEMPLATES_DIR = os.path.join(BASE_DIR, "pdf", "cover-letter-templates")
COVER_LETTER_OUTPUT_DIR = os.path.join(BASE_DIR, "uploads", "cover-letters")

os.makedirs(CV_OUTPUT_DIR, exist_ok=True)
os.makedirs(COVER_LETTER_OUTPUT_DIR, exist_ok=True)

# =========================
# PDF generators
# =========================
pdf = PDFGenerator(CV_TEMPLATES_DIR)
letters_pdf = PDFGenerator(COVER_LETTER_TEMPLATES_DIR)

# =========================
# Groq Client
# =========================
client = Groq(api_key=os.getenv("GROQ_KEY"))

# =========================
# =========================
# CV Routes
# =========================
# =========================



def get_current_user(authorization: str = Header(...)):
    """
    Decode JWT token from Authorization header.
    Expects header: Authorization: Bearer <token>
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = authorization[len("Bearer "):]  # Remove 'Bearer ' prefix

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/api/cv/preview", response_class=HTMLResponse)
def preview_cv(data: dict = Body(...)):
    template = data["template"]
    context = data["cv"]
    html = pdf.renderer.render(template, context)
    return html


@app.post("/api/cv/download")
def download_cv(data: dict = Body(...)):
    template = data["template"]
    context = data["cv"]
    filename = f"cv_{uuid.uuid4()}.pdf"
    output_path = os.path.join(CV_OUTPUT_DIR, filename)
    pdf.generate(template_name=template, output_filename=output_path, context=context)
    return FileResponse(path=output_path, filename="My_CV.pdf", media_type="application/pdf")


@app.get("/api/cv/cv-templates")
def list_cv_templates():
    try:
        templates = [
            f for f in os.listdir(CV_TEMPLATES_DIR)
            if os.path.isfile(os.path.join(CV_TEMPLATES_DIR, f)) and f.endswith(".html")
        ]
        return JSONResponse(content={"templates": templates})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# =========================
# Cover Letter Routes
# =========================
@app.post("/api/cover-letter/preview", response_class=HTMLResponse)
def preview_cover_letter(data: dict = Body(...)):
    template = data["template"]
    context = data["cover_letter"]
    html = letters_pdf.renderer.render(template, context)
    return html


@app.post("/api/cover-letter/download")
def download_cover_letter(data: dict = Body(...)):
    template = data["template"]
    context = data["cover_letter"]
    filename = f"cover_letter_{uuid.uuid4()}.pdf"
    output_path = os.path.join(COVER_LETTER_OUTPUT_DIR, filename)
    letters_pdf.generate(template_name=template, output_filename=output_path, context=context)
    return FileResponse(path=output_path, filename="My_Cover_Letter.pdf", media_type="application/pdf")


@app.get("/api/cover-letter/templates")
def list_cover_letter_templates():
    try:
        templates = [
            f for f in os.listdir(COVER_LETTER_TEMPLATES_DIR)
            if os.path.isfile(os.path.join(COVER_LETTER_TEMPLATES_DIR, f)) and f.endswith(".html")
        ]
        return JSONResponse(content={"templates": templates})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/api/cover-letter/generate-ai")
def generate_cover_letter_ai(payload: dict = Body(...)):
    context = payload.get("context", {})
    user_input = payload.get("user_input", "")

    prompt = f"""
You are a professional career assistant.

Using the information below, write a professional cover letter body
(no address header, no closing signature).

Applicant:
Name: {context.get('full_name')}
Job Title: {context.get('job_title')}
Email: {context.get('email')}
Location: {context.get('location')}

Recipient:
Company: {context.get('recipient_company')}
Position: {context.get('recipient_position')}

User Notes:
{user_input}

Rules:
- Professional tone
- Clear and concise
- 3–4 short paragraphs
- No emojis
"""
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You generate professional cover letters."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
        max_tokens=500,
    )
    return JSONResponse(content={"generated_text": completion.choices[0].message.content})


# =========================
# User Routes (Register & Login)
# =========================
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = models.User(
        username=user.username,
        password=hashed_pw.decode(),
        full_name=user.full_name,
        job_title=user.job_title,
        email=user.email,
        phone=user.phone,
        location=user.location,
        profile_summary=user.profile_summary,
        photo=user.photo
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}


@app.post("/login")
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not bcrypt.checkpw(credentials.password.encode("utf-8"), user.password.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me")
def get_my_info(current_username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return only personal info (hide password)
    return {
        "username": user.username,
        "full_name": user.full_name,
        "job_title": user.job_title,
        "email": user.email,
        "phone": user.phone,
        "location": user.location,
        "profile_summary": user.profile_summary,
        "photo": user.photo
    }



@app.post("/documents/upload")
def upload_document(file: UploadFile = File(...), current_username: str = Depends(get_current_user)):
    user_folder = os.path.join(UPLOAD_DIR, current_username)
    os.makedirs(user_folder, exist_ok=True)

    file_path = os.path.join(user_folder, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"message": "File uploaded successfully", "filename": file.filename}


@app.get("/documents")
def list_documents(current_username: str = Depends(get_current_user)):
    user_folder = os.path.join(UPLOAD_DIR, current_username)
    if not os.path.exists(user_folder):
        return {"documents": []}
    docs = os.listdir(user_folder)
    return {"documents": docs}


from fastapi import Query

@app.get("/documents/download/{filename}")
def download_document(filename: str, token: str = Query(...), db: Session = Depends(get_db)):
    try:
        # decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_folder = os.path.join(UPLOAD_DIR, username)
    file_path = os.path.join(user_folder, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)



@app.delete("/documents/delete/{filename}")
def delete_document(filename: str, current_username: str = Depends(get_current_user)):
    user_folder = os.path.join(UPLOAD_DIR, current_username)
    file_path = os.path.join(user_folder, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "File deleted"}
    raise HTTPException(status_code=404, detail="File not found")




ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs/za/search/1"


@app.get("/api/jobs/search")
def search_jobs(
    title: str = Query(..., min_length=2),
    location: str = Query("", max_length=100),
):
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": title,
        "where": location,
        "results_per_page": 20,
        "content-type": "application/json",
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return {"error": "Failed to fetch jobs"}

    data = response.json()
    return data.get("results", [])


# backend/app/routes/job_applications.py

from models import JobApplication
from schemas import JobApplicationCreate, JobApplicationOut
from typing import List


@app.post("/api/jobs/track", response_model=JobApplicationOut)
def track_job_application(app_data: JobApplicationCreate, db: Session = Depends(get_db)):
    """
    Save a job application to track.
    """
    app = JobApplication(**app_data.dict())
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


@app.get("/api/jobs/tracked", response_model=List[JobApplicationOut])
def get_tracked_jobs(db: Session = Depends(get_db)):
    """
    Get all tracked job applications (latest first).
    """
    apps = db.query(JobApplication).order_by(JobApplication.created_at.desc()).all()
    return apps


@app.patch("/api/jobs/tracked/{app_id}")
def update_job_status(app_id: int, status: str = Query(...), db: Session = Depends(get_db)):
    """
    Update the status of a tracked application.
    """
    app = db.query(JobApplication).filter(JobApplication.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    app.status = status
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

@app.patch("/api/jobs/{job_id}/status")
def update_job_status(job_id: int, status: str = Query(...), db: Session = Depends(get_db)):
    """
    Update the status of a tracked job.
    """
    job = db.query(models.JobApplication).filter(models.JobApplication.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.status = status
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@app.get("/api/jobs", response_model=List[JobApplicationOut])
def get_user_jobs(username: str = Query(...), db: Session = Depends(get_db)):
    """
    Get all jobs tracked by a specific user.
    """
    apps = db.query(models.JobApplication).filter(
        models.JobApplication.username == username
    ).order_by(models.JobApplication.created_at.desc()).all()
    return apps
# =========================
# Run server
# =========================
if __name__ == "__main__":
    uvicorn.run(
        "app:app",   # filename:FastAPI instance
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
