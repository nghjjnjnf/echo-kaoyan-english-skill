import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FETCH_SCRIPT = ROOT / "skills" / "kaoyan-english" / "scripts" / "fetch_source_article.py"
RECORD_SCRIPT = ROOT / "skills" / "kaoyan-english" / "scripts" / "record_practice.py"
SAVE_EXERCISE_SCRIPT = ROOT / "skills" / "kaoyan-english" / "scripts" / "save_exercise.py"
VALIDATE_EXERCISE_SCRIPT = ROOT / "skills" / "kaoyan-english" / "scripts" / "validate_generated_exercise.py"
VOCAB_SCRIPT = ROOT / "skills" / "kaoyan-english" / "scripts" / "check_vocabulary_coverage.py"
REVIEW_SCRIPT = ROOT / "skills" / "kaoyan-english" / "scripts" / "review_mistakes.py"
CONTRACT_SCRIPT = ROOT / "skills" / "kaoyan-english" / "scripts" / "validate_response_contract.py"


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
        self.assertEqual(data["paragraph_count"], 2)
        self.assertIn("quality_warnings", data)

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

    def test_saves_and_validates_reading_exercise_with_difficulty_mix(self):
        passage = " ".join(["Libraries help citizens use digital services responsibly."] * 75)
        questions = "\n".join(
            f"{idx}. What does the passage suggest?\n[A] A complete option.\n[B] A complete option.\n[C] A complete option.\n[D] A complete option."
            for idx in range(1, 6)
        )
        difficulty_map = {"1": "easy", "2": "medium", "3": "easy", "4": "hard", "5": "easy"}
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SAVE_EXERCISE_SCRIPT),
                    "--exercises-dir",
                    temp_dir,
                    "--title",
                    "Synthetic Exercise",
                    "--task-type",
                    "reading",
                    "--passage",
                    passage,
                    "--questions",
                    questions,
                    "--answer-key",
                    json.dumps({str(idx): "A" for idx in range(1, 6)}),
                    "--difficulty-map",
                    json.dumps(difficulty_map),
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertIn("exercise_id=", result.stdout)
            exercise_json = next(Path(temp_dir).glob("*.json"))
            subprocess.run(
                [sys.executable, str(VALIDATE_EXERCISE_SCRIPT), str(exercise_json)],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

    def test_rejects_exercise_without_challenging_items(self):
        passage = " ".join(["Libraries help citizens use digital services responsibly."] * 75)
        questions = "\n".join(
            f"{idx}. What does the passage suggest?\n[A] A complete option.\n[B] A complete option.\n[C] A complete option.\n[D] A complete option."
            for idx in range(1, 6)
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            exercise_json = Path(temp_dir) / "exercise.json"
            exercise_json.write_text(
                json.dumps(
                    {
                        "task_type": "reading",
                        "passage": passage,
                        "questions": questions,
                        "answer_key": {str(idx): "A" for idx in range(1, 6)},
                        "difficulty_map": {str(idx): "easy" for idx in range(1, 6)},
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(VALIDATE_EXERCISE_SCRIPT), str(exercise_json)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("at least 30%", result.stderr)

    def test_vocabulary_and_review_helpers(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            text = temp / "text.txt"
            vocab = temp / "vocab.txt"
            record = temp / "record.json"
            response = temp / "response.md"
            text.write_text("simple rareword simple", encoding="utf-8")
            vocab.write_text("simple\n", encoding="utf-8")
            record.write_text(
                json.dumps({"title": "r", "task_type": "reading", "user_answers": {"1": "A"}, "answer_key": {"1": "B"}}),
                encoding="utf-8",
            )
            response.write_text(
                "\n".join(["题目陷阱分类", "相关原文截取", "中文参考翻译", "完整题目", "题干在问什么", "其他选项为什么错", "为什么选择", "本题复盘"]),
                encoding="utf-8",
            )
            vocab_result = subprocess.run(
                [sys.executable, str(VOCAB_SCRIPT), str(text), "--vocab", str(vocab)],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertIn("out_of_vocab_unique=1", vocab_result.stdout)
            review_result = subprocess.run(
                [sys.executable, str(REVIEW_SCRIPT), str(record)],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertIn("wrong=1", review_result.stdout)
            subprocess.run(
                [sys.executable, str(CONTRACT_SCRIPT), str(response), "--type", "reading"],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )


if __name__ == "__main__":
    unittest.main()
