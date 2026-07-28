#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "kaoyan-english"


def resolve_codex_home(value):
    if value:
        return Path(value).expanduser().resolve()
    if os.environ.get("CODEX_HOME"):
        return Path(os.environ["CODEX_HOME"]).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def ensure_safe_destination(codex_home):
    skills_dir = (codex_home / "skills").resolve()
    destination = (skills_dir / "kaoyan-english").resolve()
    if destination.name != "kaoyan-english":
        raise ValueError(f"unexpected destination name: {destination}")
    if skills_dir not in destination.parents:
        raise ValueError(f"destination is outside Codex skills directory: {destination}")
    return skills_dir, destination


def copy_skill(destination):
    if not SOURCE.is_dir():
        raise FileNotFoundError(f"missing source skill directory: {SOURCE}")
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(SOURCE, destination)


def install_dependencies(skip_deps):
    if skip_deps:
        return
    requirements = ROOT / "requirements.txt"
    if requirements.is_file():
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements)], check=True)


def validate_install(codex_home, destination, no_validate):
    if no_validate:
        return
    validator = codex_home / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    if not validator.is_file():
        print(f"warning: quick_validate.py not found at {validator}; copied skill but skipped validation.")
        return
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    subprocess.run([sys.executable, str(validator), str(destination)], check=True, env=env)


def main():
    parser = argparse.ArgumentParser(description="Install Echo_考研英语SKILL into the local Codex skills directory.")
    parser.add_argument("--codex-home", help="Override Codex home. Defaults to CODEX_HOME or ~/.codex.")
    parser.add_argument("--skip-deps", action="store_true", help="Do not install Python dependencies.")
    parser.add_argument("--no-validate", action="store_true", help="Skip quick_validate.py after copying.")
    args = parser.parse_args()

    codex_home = resolve_codex_home(args.codex_home)
    skills_dir, destination = ensure_safe_destination(codex_home)
    skills_dir.mkdir(parents=True, exist_ok=True)
    copy_skill(destination)
    install_dependencies(args.skip_deps)
    validate_install(codex_home, destination, args.no_validate)
    print(f"Installed kaoyan-english skill to {destination}")


if __name__ == "__main__":
    main()
