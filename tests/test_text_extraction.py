import unittest
from pathlib import Path

from resume_analyzer.text_extraction import (
    allowed_file,
    extract_resume_text,
    normalize_text,
)


class FileValidationTest(unittest.TestCase):
    def test_allows_supported_resume_formats(self):
        self.assertTrue(allowed_file("resume.pdf"))
        self.assertTrue(allowed_file("resume.docx"))
        self.assertTrue(allowed_file("resume.txt"))
        self.assertTrue(allowed_file("RESUME.PDF"))

    def test_rejects_unsupported_or_extensionless_files(self):
        self.assertFalse(allowed_file("resume.png"))
        self.assertFalse(allowed_file("resume"))
        self.assertFalse(allowed_file(""))


class TextNormalizationTest(unittest.TestCase):
    def test_normalizes_spacing_and_null_bytes(self):
        text = normalize_text("  Alex\x00   Morgan\n\n\n\nPython\tDeveloper  ")

        self.assertEqual(text, "Alex Morgan\n\nPython Developer")


class TextExtractionTest(unittest.TestCase):
    def test_extracts_txt_resume_text(self):
        text = extract_resume_text(Path("requirements.txt"))

        self.assertIn("Flask", text)
        self.assertIn("pdfminer.six", text)

    def test_raises_for_unsupported_extension(self):
        with self.assertRaises(ValueError):
            extract_resume_text(Path("README.md"))


if __name__ == "__main__":
    unittest.main()
