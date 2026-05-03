# AI Resume Analyzer

A professional Flask web app that analyzes resumes and produces an ATS-style score with keyword matching, skill detection, section checks, and practical improvement suggestions.

## Features

- Upload resumes as PDF, DOCX, or TXT
- Paste a target job description for sharper keyword matching
- Get an ATS-style score out of 100
- Review score breakdown across contact details, sections, keywords, impact, readability, and length
- Detect technical and professional skills by category
- Find missing job-description keywords
- Get prioritized resume improvement suggestions
- Preview parsed resume text
- Uploaded files are removed after analysis

## Tech Stack

- Python
- Flask
- pdfminer.six
- python-docx
- HTML and CSS

## Project Structure

```text
resume-analyzer/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── templates/
│   ├── index.html
│   └── result.html
└── uploads/
    └── .gitkeep
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
flask --app app run
```

Open:

```text
http://127.0.0.1:5000/
```

## Development

To run with Flask debug mode:

```bash
set FLASK_DEBUG=1
flask --app app run
```

On macOS/Linux:

```bash
FLASK_DEBUG=1 flask --app app run
```

## Notes

This app performs local, explainable resume analysis. It does not send resumes to an external AI service. The scoring logic is heuristic and intended to help improve resume structure, ATS readability, keyword alignment, and achievement clarity.

## License

This project is licensed under the MIT License.
