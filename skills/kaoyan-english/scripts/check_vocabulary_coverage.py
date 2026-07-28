#!/usr/bin/env python3
import argparse
import re
from collections import Counter
from pathlib import Path


def load_vocab(paths):
    words = set()
    for path in paths:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            word = line.strip().lower()
            if word and not word.startswith("#"):
                words.add(word)
    return words


def tokenize(text):
    return [item.lower() for item in re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text)]


def main():
    parser = argparse.ArgumentParser(description="Check vocabulary coverage for a generated passage.")
    parser.add_argument("text_file")
    parser.add_argument("--vocab", nargs="+", required=True, help="One or more UTF-8 vocabulary files.")
    parser.add_argument("--top", type=int, default=30)
    args = parser.parse_args()

    vocab = load_vocab(args.vocab)
    tokens = tokenize(Path(args.text_file).read_text(encoding="utf-8"))
    unique = sorted(set(tokens))
    out = [word for word in unique if word not in vocab]
    counts = Counter(token for token in tokens if token not in vocab)
    coverage = 0.0 if not unique else (len(unique) - len(out)) / len(unique) * 100

    print(f"tokens={len(tokens)}")
    print(f"unique_words={len(unique)}")
    print(f"in_vocab_unique={len(unique) - len(out)}")
    print(f"out_of_vocab_unique={len(out)}")
    print(f"coverage_percent={coverage:.2f}")
    print("top_out_of_vocab=")
    for word, count in counts.most_common(args.top):
        print(f"{word}\t{count}")


if __name__ == "__main__":
    main()
