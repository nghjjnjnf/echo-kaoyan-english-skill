import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
IMPORT_SCRIPT = ROOT / "skills" / "kaoyan-english" / "scripts" / "import_docx_papers.py"


class ImportDocxTest(unittest.TestCase):
    def test_imports_synthetic_english_i_paper(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            docx_path = temp / "synthetic.docx"
            skill = temp / "skill"
            document = Document()
            paragraphs = [
                "2010英一",
                "Section I Use of English",
                "1. Synthetic cloze item.",
                "Section II Reading Comprehension",
                "Part A",
                "Text 1",
                "Synthetic passage.",
                "21. Synthetic question?",
                "[A] First [B] Second [C] Third [D] Fourth",
                "Part B",
                "41. Synthetic matching item.",
                "Part C",
                "46. Synthetic translation segment.",
                "Section III Writing",
                "51. Synthetic writing prompt.",
                "2010 年全国硕士研究生招生考试英语（一）试题参考答案",
                "Section I Use of English",
                "1. A",
                "Section II Reading Comprehension",
                "Text 1 21. B",
                "Part B",
                "1. C",
                "Part C",
                "46. 参考译文",
                "Section III Writing",
            ]
            for paragraph in paragraphs:
                document.add_paragraph(paragraph)
            document.save(docx_path)

            result = subprocess.run(
                [
                    sys.executable,
                    str(IMPORT_SCRIPT),
                    str(docx_path),
                    "--skill",
                    str(skill),
                    "--exam",
                    "english-i",
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            year_dir = skill / "references" / "papers" / "english-i" / "2010"
            answers = json.loads((year_dir / "answers.json").read_text(encoding="utf-8"))
            index = json.loads((skill / "references" / "corpus-index.json").read_text(encoding="utf-8"))
            reading_file_exists = (year_dir / "reading-text-1.md").is_file()

        self.assertIn("Imported years: 2010", result.stdout)
        self.assertEqual(answers["answers"]["reading-text-1"]["21"], "B")
        self.assertIn("2010", index["english-i"])
        self.assertTrue(reading_file_exists)


if __name__ == "__main__":
    unittest.main()
