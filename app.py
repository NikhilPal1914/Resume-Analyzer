import os
import uuid
from pathlib import Path

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from resume_analyzer import (
    allowed_file,
    analyze_resume_with_local_ai,
    extract_resume_text,
    score_resume,
)


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    resume_file = request.files.get("resume")
    job_description = request.form.get("job_description", "").strip()

    if not resume_file or not resume_file.filename:
        return render_template("index.html", error="Please upload a resume file.")

    if not allowed_file(resume_file.filename):
        return render_template("index.html", error="Upload a PDF, DOCX, or TXT resume.")

    original_name = secure_filename(resume_file.filename)
    extension = Path(original_name).suffix.lower()
    saved_path = UPLOAD_DIR / f"{uuid.uuid4().hex}{extension}"

    try:
        resume_file.save(saved_path)
        text = extract_resume_text(saved_path)
        if len(text) < 80:
            return render_template(
                "index.html",
                error="I could not read enough text from that file. Try a text-based PDF, DOCX, or TXT resume.",
            )

        analysis = score_resume(text, job_description)
        analysis["ai"] = analyze_resume_with_local_ai(text, job_description, analysis)
        return render_template("result.html", analysis=analysis, filename=original_name)
    except Exception as exc:
        return render_template("index.html", error=f"Could not analyze the resume: {exc}")
    finally:
        if saved_path.exists():
            saved_path.unlink()


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    app.run(debug=debug)
