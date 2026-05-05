# AI Resume Analyzer

A professional Flask web app that analyzes resumes and produces an ATS-style score with keyword matching, skill detection, section checks, and practical improvement suggestions.

## Features

- Upload resumes as PDF, DOCX, or TXT
- Paste a target job description for sharper keyword matching
- Get an ATS-style score out of 100
- Review score breakdown across contact details, sections, keywords, impact, readability, and length
- Detect technical and professional skills by category
- Find missing job-description keywords
- Review local AI/NLP insights without an external API
- Get prioritized resume improvement suggestions
- Preview parsed resume text
- Uploaded files are removed after analysis

## Tech Stack

- Python
- Flask
- pdfminer.six
- python-docx
- unittest
- HTML and CSS

## Project Structure

```text
resume-analyzer/
|-- app.py
|-- requirements.txt
|-- README.md
|-- LICENSE
|-- resume_analyzer/
|   |-- __init__.py
|   |-- ai_analysis.py
|   |-- analysis.py
|   |-- constants.py
|   `-- text_extraction.py
|-- templates/
|   |-- index.html
|   `-- result.html
|-- tests/
|   |-- test_analysis.py
|   |-- test_app.py
|   `-- test_text_extraction.py
`-- uploads/
    `-- .gitkeep
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

To run with Flask debug mode on Windows:

```bash
set FLASK_DEBUG=1
flask --app app run
```

On macOS/Linux:

```bash
FLASK_DEBUG=1 flask --app app run
```

Run the Python test suite:

```bash
python -m unittest discover -s tests
```

## Python-first Layout

The Flask entry point in `app.py` stays intentionally small. Resume parsing, scoring, skill detection, keyword matching, and suggestion logic live in the `resume_analyzer` package so the project is easier to test and extend from Python.

## Local AI

The project uses a local AI-style NLP layer in `resume_analyzer/ai_analysis.py`.

It does not use the OpenAI API.

It does not require an API key.

It compares resume text with the target job description, estimates fit, detects strengths and concerns, and writes a suggested summary.

The HTML templates are marked as non-detectable in `.gitattributes` so GitHub language statistics focus on the Python application code.

## Notes

This app performs local, explainable resume analysis. It does not send resumes to an external AI service. The scoring logic is heuristic and intended to help improve resume structure, ATS readability, keyword alignment, and achievement clarity.

## License

This project is licensed under the MIT License.
