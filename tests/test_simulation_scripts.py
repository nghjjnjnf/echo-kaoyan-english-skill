import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FETCH_SCRIPT = ROOT / "skills" / "kaoyan-english" / "scripts" / "fetch_source_article.py"
RECORD_SCRIPT = ROOT / "skills" / "kaoyan-english" / "scripts" / "record_practice.py"


class SimulationScriptsTest(unittest.TestCase):
    def test_extracts_whitelisted_article_from_html_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            html_path = Path(temp_dir) / "article.html"
            html_path.write_text(
                """
                <html><head><title>Clean Energy Choices</title></head>
                <body>
                  <p>Short.</p>
                  <p>Many communities are looking for simple ways to save energy while keeping daily life comfortable.</p>
                  <p>Local schools and libraries often become useful places for sharing practical ideas with families.</p>
                </body></html>
                """,
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(FETCH_SCRIPT),
                    "https://learningenglish.voanews.com/a/example.html",
                    "--html-file",
                    str(html_path),
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        data = json.loads(result.stdout)
        self.assertEqual(data["source_mode"], "adaptable")
        self.assertEqual(data["title"], "Clean Energy Choices")
        self.assertEqual(len(data["paragraphs"]), 2)

    def test_saves_practice_record(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            record = {
                "title": "Synthetic Reading",
                "task_type": "reading",
                "passage": "This is a synthetic passage.",
                "questions": "1. What is the passage about?",
                "user_answers": {"1": "A"},
                "answer_key": {"1": "A"},
                "analysis": "A is correct because it matches the main idea.",
                "created_at": "2026-01-01T00:00:00",
            }
            result = subprocess.run(
                [
                    sys.executable,
                    str(RECORD_SCRIPT),
                    "--records-dir",
                    temp_dir,
                    "--record-json",
                    json.dumps(record, ensure_ascii=False),
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertIn("json=", result.stdout)
            self.assertIn("markdown=", result.stdout)
            self.assertEqual(len(list(Path(temp_dir).glob("*.json"))), 1)
            markdown_files = list(Path(temp_dir).glob("*.md"))
            self.assertEqual(len(markdown_files), 1)
            self.assertIn("## 标准答案", markdown_files[0].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
