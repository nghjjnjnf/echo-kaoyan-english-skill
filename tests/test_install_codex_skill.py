import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALL_SCRIPT = ROOT / "scripts" / "install_codex_skill.py"


class InstallCodexSkillTest(unittest.TestCase):
    def test_installs_skill_into_custom_codex_home(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            subprocess.run(
                [
                    sys.executable,
                    str(INSTALL_SCRIPT),
                    "--codex-home",
                    temp_dir,
                    "--skip-deps",
                    "--no-validate",
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            installed = Path(temp_dir) / "skills" / "kaoyan-english"
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "references" / "rubrics" / "reading-analysis.md").is_file())


if __name__ == "__main__":
    unittest.main()
