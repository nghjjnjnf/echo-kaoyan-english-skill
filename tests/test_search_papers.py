import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEARCH_SCRIPT = ROOT / "skills" / "kaoyan-english" / "scripts" / "search_papers.py"
BUILD_INDEX_SCRIPT = ROOT / "skills" / "kaoyan-english" / "scripts" / "build_index.py"


class SearchPapersTest(unittest.TestCase):
    def test_locates_question_and_answer(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = Path(temp_dir)
            year_dir = skill / "references" / "papers" / "english-i" / "2025"
            year_dir.mkdir(parents=True)
            (year_dir / "meta.json").write_text(
                json.dumps({"sections": ["reading-text-1"]}),
                encoding="utf-8",
            )
            (year_dir / "question-map.json").write_text(
                json.dumps({"21": {"section": "reading-text-1", "file": "reading-text-1.md"}}),
                encoding="utf-8",
            )
            (year_dir / "answers.json").write_text(
                json.dumps({"answers": {"reading-text-1": {"21": "A"}}}),
                encoding="utf-8",
            )
            (year_dir / "reading-text-1.md").write_text("# Synthetic fixture\n", encoding="utf-8")
            (skill / "references" / "corpus-index.json").write_text(
                json.dumps({"english-i": {"2025": {"path": "references/papers/english-i/2025", "sections": ["reading-text-1"]}}}),
                encoding="utf-8",
            )
            subprocess.run(
                [sys.executable, str(BUILD_INDEX_SCRIPT), "--skill", str(skill)],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SEARCH_SCRIPT),
                    "--skill",
                    str(skill),
                    "--exam",
                    "english-i",
                    "--year",
                    "2025",
                    "--question",
                    "21",
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertTrue((skill / "references" / "index.json").is_file())

        self.assertIn("section=reading-text-1", result.stdout)
        self.assertIn("answer=A", result.stdout)


if __name__ == "__main__":
    unittest.main()
