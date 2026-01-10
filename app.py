from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse, FileResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pdf.generator import PDFGenerator
import os
import uuid
import uvicorn

app = FastAPI(title="CV Generator API")

# CORS (for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "pdf", "templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "uploads", "certificates")

os.makedirs(OUTPUT_DIR, exist_ok=True)

pdf = PDFGenerator(TEMPLATES_DIR)

@app.post("/api/cv/preview", response_class=HTMLResponse)
def preview_cv(data: dict = Body(...)):
    """
    Returns rendered HTML for live preview
    """
    template = data["template"]
    context = data["cv"]

    html = pdf.renderer.render(template, context)
    return html

@app.post("/api/cv/download")
def download_cv(data: dict = Body(...)):
    """
    Generates and returns the CV PDF
    """
    template = data["template"]
    context = data["cv"]

    filename = f"cv_{uuid.uuid4()}.pdf"
    output_path = os.path.join(OUTPUT_DIR, filename)

    pdf.generate(
        template_name=template,
        output_filename=output_path,
        context=context,
    )

    return FileResponse(
        path=output_path,
        filename="My_CV.pdf",
        media_type="application/pdf"
    )

@app.get("/api/cv/templates")
def list_templates():
    """
    Returns a list of all CV template filenames in the templates folder
    """
    try:
        templates = [
            f for f in os.listdir(TEMPLATES_DIR)
            if os.path.isfile(os.path.join(TEMPLATES_DIR, f)) and f.endswith(".html")
        ]
        return JSONResponse(content={"templates": templates})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":

    uvicorn.run(
        "app:app",   # 👈 filename:FastAPI instance
        host="0.0.0.0",
        port=8000,
        reload=True
    )
