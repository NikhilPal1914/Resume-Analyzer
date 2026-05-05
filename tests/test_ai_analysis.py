import unittest

from resume_analyzer.ai_analysis import analyze_resume_with_local_ai
from resume_analyzer.analysis import score_resume


RESUME_TEXT = """
Alex Morgan
alex@example.com

Summary:
Python developer building Flask analytics tools.

Skills:
Python, Flask, SQL, PostgreSQL, Docker, Git

Experience:
- Built Flask dashboards for 500 users and reduced reporting time by 35%.
- Automated reports for 12 projects using Python and SQL.
"""


class LocalAIAnalysisTest(unittest.TestCase):
    def test_returns_local_ai_review(self):
        base = score_resume(RESUME_TEXT, "Python Flask PostgreSQL Docker dashboards")

        result = analyze_resume_with_local_ai(
            RESUME_TEXT,
            "Python Flask PostgreSQL Docker dashboards",
            base,
        )

        self.assertTrue(result["enabled"])
        self.assertEqual(result["engine"], "Local NLP AI")
        self.assertGreater(result["fit_score"], 0)
        self.assertTrue(result["summary"])
        self.assertTrue(result["strengths"])
        self.assertTrue(result["priority_actions"])
        self.assertIn("candidate", result["rewritten_summary"].lower())


if __name__ == "__main__":
    unittest.main()
