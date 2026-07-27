#!/usr/bin/env python3
import argparse
import json
import re
import shutil
from pathlib import Path

from docx import Document


PAGE_MARK_RE = re.compile(r"英语（[一二]）试题\s*-\d+-\s*（共\s*\d+\s*页）.*?(?=(?:公\s*众\s*号|公众号|$))")
WECHAT_RE = re.compile(
    r"【?\s*公\s*众\s*号\s*[：:]\s*猫\s*叔\s*考\s*研\s*英\s*语\s*】?"
    r"|【?\s*公众号\s*[：:]\s*猫叔考研英语\s*】?"
    r"|猫\s*叔\s*考\s*研\s*英\s*语"
)
YEAR_START_RE = re.compile(r"^(?:(20\d{2})英[一二]|(20\d{2})\s*年全国硕士研究生招生考试英语（[一二]）(?:试题)?)$")
ANSWER_MARK_RE = re.compile(r"(20\d{2})\s*年全国硕士研究生招生考试英语（[一二]）试题参考答案")

EXAM_LABELS = {
    "english-i": "考研英语一",
    "english-ii": "考研英语二",
}


def clean_line(text):
    text = PAGE_MARK_RE.sub("", text)
    text = WECHAT_RE.sub("", text)
    text = text.replace("】", "")
    text = text.replace("【", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def read_docx_lines(path):
    doc = Document(path)
    lines = []
    for paragraph in doc.paragraphs:
        text = clean_line(paragraph.text)
        if text:
            lines.append(text)
    return lines


def split_year_blocks(lines):
    starts = []
    for idx, line in enumerate(lines):
        match = YEAR_START_RE.match(line)
        if match:
            starts.append((idx, match.group(1) or match.group(2)))
    blocks = {}
    for pos, (start, year) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        blocks[year] = lines[start:end]
    return blocks


def split_answer(lines, year):
    joined = "\n".join(lines)
    match = ANSWER_MARK_RE.search(joined)
    if not match:
        return joined.strip(), ""
    return joined[: match.start()].strip(), joined[match.end() :].strip()


def find_section(text, start_pat, end_pat=None):
    start = re.search(start_pat, text, flags=re.I)
    if not start:
        return ""
    end = re.search(end_pat, text[start.end() :], flags=re.I) if end_pat else None
    if end:
        return text[start.start() : start.end() + end.start()].strip()
    return text[start.start() :].strip()


def split_reading_part_a(reading_text):
    chunks = {}
    matches = list(re.finditer(r"(?m)^Text\s+([1-4])\s*$", reading_text))
    for i, match in enumerate(matches):
        text_no = match.group(1)
        end = matches[i + 1].start() if i + 1 < len(matches) else len(reading_text)
        chunks[f"reading-text-{text_no}"] = reading_text[match.start() : end].strip()
    return chunks


def md(title, body):
    return f"# {title}\n\n{body.strip()}\n"


def parse_choice_answers(answer_text):
    answers = {
        "cloze": {},
        "reading-text-1": {},
        "reading-text-2": {},
        "reading-text-3": {},
        "reading-text-4": {},
        "new-question-type": {},
        "translation": {},
        "writing": {},
    }

    current = None
    for raw in answer_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if re.search(r"Section I Use of English", line, re.I):
            current = "cloze"
            continue
        if re.search(r"Section II Reading Comprehension", line, re.I):
            current = None
            continue
        text_match = re.match(r"Text\s+([1-4])\s+(.+)$", line)
        if text_match:
            section = f"reading-text-{text_match.group(1)}"
            for num, ans in re.findall(r"(\d{1,2})\.\s*([A-D])", text_match.group(2)):
                answers[section][num] = ans
            continue
        if re.search(r"Part B", line, re.I):
            current = "new-question-type"
            continue
        if re.search(r"Part C", line, re.I):
            current = "translation"
            continue
        if re.search(r"Section III Writing", line, re.I):
            current = "writing"
            continue

        if current == "cloze":
            for num, ans in re.findall(r"(\d{1,2})\.\s*([A-D])", line):
                answers[current][num] = ans
        if current == "new-question-type":
            for num, ans in re.findall(r"(\d{1,2})\.\s*([A-GTF])", line):
                if int(num) < 10:
                    num = str(40 + int(num))
                answers[current][num] = ans

    # Parse translation references as multi-line values.
    translation_block = ""
    part_c = re.search(r"Part C\s*(.*?)(?:Section III Writing|$)", answer_text, flags=re.S | re.I)
    section_iii = re.search(r"Section III Translation\s*(.*?)(?:Section IV Writing|$)", answer_text, flags=re.S | re.I)
    if part_c:
        translation_block = part_c.group(1).strip()
    elif section_iii:
        translation_block = section_iii.group(1).strip()
    current_num = None
    for line in translation_block.splitlines():
        m = re.match(r"^(4[6-9]|50)\.\s*(.*)$", line.strip())
        if m:
            current_num = m.group(1)
            answers["translation"][current_num] = m.group(2).strip()
        elif current_num:
            answers["translation"][current_num] = (answers["translation"][current_num] + " " + line.strip()).strip()

    for num, note in re.findall(r"(4[78]|5[12])\.\s*([^\n]+)", answer_text):
        answers["writing"][num] = note.strip()

    # Some answer keys omit writing answers because the section is "略"; keep
    # the question map usable for lookups anyway.
    if re.search(r"Section IV Writing", answer_text, flags=re.I):
        answers["writing"].setdefault("47", "见题目")
        answers["writing"].setdefault("48", "见题目")
    if re.search(r"Section III Writing", answer_text, flags=re.I):
        answers["writing"].setdefault("51", "见题目")
        answers["writing"].setdefault("52", "见题目")

    return answers


def build_question_map(answers):
    qmap = {}
    files = {
        "cloze": "cloze.md",
        "reading-text-1": "reading-text-1.md",
        "reading-text-2": "reading-text-2.md",
        "reading-text-3": "reading-text-3.md",
        "reading-text-4": "reading-text-4.md",
        "new-question-type": "new-question-type.md",
        "translation": "translation.md",
        "writing": "writing.md",
    }
    for section, section_answers in answers.items():
        for num in section_answers:
            qmap[str(num)] = {"section": section, "file": files[section]}
    return dict(sorted(qmap.items(), key=lambda item: int(item[0])))


def write_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def import_docx(docx_path, skill_path, exam):
    lines = read_docx_lines(docx_path)
    blocks = split_year_blocks(lines)
    if not blocks:
        raise SystemExit("No year blocks found. Expected headings like '2010英一'.")

    papers_root = skill_path / "references" / "papers" / exam
    papers_root.mkdir(parents=True, exist_ok=True)
    raw_dir = skill_path / "assets" / "raw-papers" / exam
    raw_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(docx_path, raw_dir / Path(docx_path).name)

    corpus_index_path = skill_path / "references" / "corpus-index.json"
    if corpus_index_path.exists():
        corpus_index = json.loads(corpus_index_path.read_text(encoding="utf-8"))
    else:
        corpus_index = {}
    corpus_index.setdefault(exam, {})

    imported = []
    for year, block_lines in blocks.items():
        paper_text, answer_text = split_answer(block_lines, year)
        year_dir = papers_root / year
        year_dir.mkdir(parents=True, exist_ok=True)
        label = EXAM_LABELS[exam]

        cloze = find_section(paper_text, r"(?m)^Section I Use of English$", r"(?m)^Section II Reading Comprehension$")
        reading_all = find_section(paper_text, r"(?m)^Part A$", r"(?m)^Part B$")
        reading_chunks = split_reading_part_a(reading_all)
        if exam == "english-ii":
            new_question_type = find_section(paper_text, r"(?m)^Part B$", r"(?m)^Section III Translation$")
            translation = find_section(paper_text, r"(?m)^Section III Translation$", r"(?m)^Section IV Writing$")
            writing = find_section(paper_text, r"(?m)^Section IV Writing$")
        else:
            new_question_type = find_section(paper_text, r"(?m)^Part B$", r"(?m)^Part C$")
            translation = find_section(paper_text, r"(?m)^Part C$", r"(?m)^Section III Writing$")
            writing = find_section(paper_text, r"(?m)^Section III Writing$")

        sections = []
        section_payloads = {
            "paper": md(f"{year} {label}完整试题", paper_text),
            "cloze": md(f"{year} {label} Section I Use of English", cloze),
            "new-question-type": md(f"{year} {label} Section II Part B", new_question_type),
            "translation": md(f"{year} {label} Translation", translation),
            "writing": md(f"{year} {label} Writing", writing),
        }
        for key, value in reading_chunks.items():
            section_payloads[key] = md(f"{year} {label} {key.replace('-', ' ').title()}", value)

        order = [
            "paper",
            "cloze",
            "reading-text-1",
            "reading-text-2",
            "reading-text-3",
            "reading-text-4",
            "new-question-type",
            "translation",
            "writing",
        ]
        for key in order:
            if key in section_payloads and section_payloads[key].strip() != f"# {year} {label}\n":
                (year_dir / f"{key}.md").write_text(section_payloads[key], encoding="utf-8")
                if key != "paper":
                    sections.append(key)

        answers = parse_choice_answers(answer_text)
        write_json(year_dir / "answers.json", {"exam": exam, "year": int(year), "answers": answers})
        write_json(year_dir / "question-map.json", build_question_map(answers))
        write_json(
            year_dir / "meta.json",
            {
                "exam": exam,
                "year": int(year),
                "source_docx": str(raw_dir / Path(docx_path).name),
                "sections": sections,
            },
        )
        corpus_index[exam][year] = {
            "path": f"references/papers/{exam}/{year}",
            "sections": sections,
            "source": f"assets/raw-papers/{exam}/{Path(docx_path).name}",
        }
        imported.append(year)

    write_json(corpus_index_path, corpus_index)
    return imported


def main():
    parser = argparse.ArgumentParser(description="Import kaoyan English DOCX papers into skill resources.")
    parser.add_argument("docx")
    parser.add_argument("--skill", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--exam", default="english-i", choices=["english-i", "english-ii"])
    args = parser.parse_args()

    imported = import_docx(Path(args.docx), Path(args.skill), args.exam)
    print("Imported years:", ", ".join(imported))


if __name__ == "__main__":
    main()
