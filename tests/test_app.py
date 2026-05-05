import io
import unittest

from app import app


VALID_RESUME_TEXT = """
Alex Morgan
alex@example.com | +91 98765 43210 | linkedin.com/in/alexmorgan | github.com/alexmorgan

Summary:
Python developer building Flask resume analysis tools.

Skills:
Python, Flask, SQL, PostgreSQL, Git, Docker, Pandas, Communication

Experience:
- Built Flask dashboards for 500 users and reduced reporting time by 35%.
- Automated resume screening workflows for 12 projects using Python and SQL.
- Improved API reliability by 20% through better validation and tests.
- Delivered analytics reports for 8 business teams.

Education:
B.Tech Computer Science

Projects:
Resume Analyzer with ATS keyword matching.
""".strip()


class FlaskRouteTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Analyze Resume", response.data)

    def test_analyze_requires_file(self):
        response = self.client.post("/analyze", data={})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please upload a resume file.", response.data)

    def test_analyze_rejects_unsupported_file(self):
        response = self.client.post(
            "/analyze",
            data={"resume": (io.BytesIO(b"not a resume"), "resume.png")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Upload a PDF, DOCX, or TXT resume.", response.data)

    def test_analyze_txt_resume_renders_result(self):
        response = self.client.post(
            "/analyze",
            data={
                "resume": (io.BytesIO(VALID_RESUME_TEXT.encode("utf-8")), "resume.txt"),
                "job_description": "Python Flask PostgreSQL Docker dashboards automation testing",
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ATS Resume Report", response.data)
        self.assertIn(b"Local AI Insights", response.data)
        self.assertIn(b"resume.txt", response.data)


if __name__ == "__main__":
    unittest.main()
