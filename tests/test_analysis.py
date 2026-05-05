import unittest

from resume_analyzer.analysis import (
    count_action_verbs,
    count_quantified_results,
    extract_job_keywords,
    extract_skills,
    find_contact_details,
    find_sections,
    grade_for_score,
    match_keywords,
    score_resume,
)


SAMPLE_RESUME = """
Alex Morgan
alex@example.com | +91 98765 43210
linkedin.com/in/alexmorgan | github.com/alexmorgan

Summary:
Python developer focused on Flask APIs, automation, and data analysis.

Skills:
Python, Flask, SQL, PostgreSQL, Git, Docker, Pandas, Communication

Experience:
- Built Flask dashboards for 500 users and reduced reporting time by 35%.
- Automated resume screening workflows for 12 projects using Python and SQL.
- Improved API reliability by 20% through better validation and tests.
- Delivered analytics reports for 8 business teams.

Education:
Bachelor of Technology in Computer Science

Projects:
Resume Analyzer - created an ATS scoring app with keyword matching.
"""


class ContactParsingTest(unittest.TestCase):
    def test_finds_contact_links(self):
        contact = find_contact_details(SAMPLE_RESUME)

        self.assertEqual(contact["email"], "alex@example.com")
        self.assertEqual(contact["phone"], "+91 98765 43210")
        self.assertEqual(contact["linkedin"], "linkedin.com/in/alexmorgan")
        self.assertEqual(contact["portfolio"], "github.com/alexmorgan")

    def test_missing_contact_values_are_none(self):
        contact = find_contact_details("No contact details here")

        self.assertIsNone(contact["email"])
        self.assertIsNone(contact["phone"])
        self.assertIsNone(contact["linkedin"])
        self.assertIsNone(contact["portfolio"])


class SectionParsingTest(unittest.TestCase):
    def test_detects_standard_resume_sections(self):
        found, missing = find_sections(SAMPLE_RESUME)

        self.assertIn("Summary", found)
        self.assertIn("Skills", found)
        self.assertIn("Experience", found)
        self.assertIn("Education", found)
        self.assertIn("Projects", found)
        self.assertNotIn("Skills", missing)

    def test_reports_missing_sections(self):
        found, missing = find_sections("Skills: Python, Flask")

        self.assertEqual(found, ["Skills"])
        self.assertIn("Experience", missing)
        self.assertIn("Education", missing)


class SkillExtractionTest(unittest.TestCase):
    def test_extracts_skills_by_category(self):
        categories, flat = extract_skills(SAMPLE_RESUME)

        self.assertIn("Programming", categories)
        self.assertIn("Frameworks", categories)
        self.assertIn("Databases", categories)
        self.assertIn("python", flat)
        self.assertIn("flask", flat)
        self.assertIn("postgresql", flat)

    def test_skill_matching_respects_boundaries(self):
        _, flat = extract_skills("I write scripts in python, not pythonesque prose.")

        self.assertEqual(flat, ["python"])


class KeywordMatchingTest(unittest.TestCase):
    def test_extracts_job_keywords_from_skills_and_common_terms(self):
        keywords = extract_job_keywords(
            "We need Python, Flask, PostgreSQL, dashboards, automation, and testing."
        )

        self.assertIn("python", keywords)
        self.assertIn("flask", keywords)
        self.assertIn("postgresql", keywords)
        self.assertIn("dashboards", keywords)

    def test_matches_and_reports_missing_keywords(self):
        matched, missing = match_keywords(
            "Python developer with Flask experience.",
            "Python Flask Docker PostgreSQL",
        )

        self.assertIn("python", matched)
        self.assertIn("flask", matched)
        self.assertIn("docker", missing)
        self.assertIn("postgresql", missing)


class ScoringSignalTest(unittest.TestCase):
    def test_counts_action_verbs(self):
        count = count_action_verbs("Built tools, automated reports, and improved APIs.")

        self.assertEqual(count, 3)

    def test_counts_quantified_results(self):
        count = count_quantified_results(
            "Reduced time by 35%, served 500 users, handled 12 projects, saved $2000."
        )

        self.assertEqual(count, 4)

    def test_grade_boundaries(self):
        self.assertEqual(grade_for_score(85), "Excellent")
        self.assertEqual(grade_for_score(70), "Strong")
        self.assertEqual(grade_for_score(55), "Needs polish")
        self.assertEqual(grade_for_score(54), "Needs work")


class ResumeScoreTest(unittest.TestCase):
    def test_score_resume_returns_expected_report_shape(self):
        report = score_resume(
            SAMPLE_RESUME,
            "Python Flask PostgreSQL Docker dashboards automation testing",
        )

        self.assertGreaterEqual(report["score"], 70)
        self.assertEqual(report["grade"], "Strong")
        self.assertEqual(report["contact"]["email"], "alex@example.com")
        self.assertIn("python", report["skills"])
        self.assertIn("docker", report["matched_keywords"])
        self.assertIn("testing", report["missing_keywords"])
        self.assertEqual(len(report["breakdown"]), 6)
        self.assertTrue(report["suggestions"])

    def test_score_resume_without_job_description_uses_detected_skills(self):
        report = score_resume(SAMPLE_RESUME)

        self.assertEqual(report["matched_keywords"], [])
        self.assertEqual(report["missing_keywords"], [])
        self.assertGreater(report["breakdown"][2]["score"], 0)


if __name__ == "__main__":
    unittest.main()
