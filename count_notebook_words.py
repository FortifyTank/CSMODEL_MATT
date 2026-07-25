#!/usr/bin/env python3
"""
count_notebook_words.py

Counts the number of words in the text (markdown/raw) cells of a Jupyter
notebook (.ipynb file), ignoring code cells.

By default it only counts markdown cells (skipping code cells and outputs),
strips Markdown syntax (headers, links, code spans, etc.) so it doesn't pad the
count, and prints total words/characters. You can pass multiple .ipynb files at
once, and it'll give you a grand total. Useful options:

    --include-raw — also count "raw" cells
    --verbose — show a per-cell word/char breakdown
    --keep-markdown-syntax — count raw markdown source as-is, without stripping #, *, links, etc.

Usage:
    python count_notebook_words.py notebook.ipynb
    python count_notebook_words.py notebook.ipynb --verbose
    python count_notebook_words.py notebook1.ipynb notebook2.ipynb


DISCLAIMER: Generated with Claude AI. Tweaked with Claude AI as some edge cases
appeared after testing. Not guaranteed to be perfect, but should be good enough.
If you find any issues, please report them to the kristine.kalaw@dlsu.edu.ph
"""

import argparse
import json
import re
import sys
from pathlib import Path


def get_cell_source_text(cell):
    """Return the source of a cell as a single string, handling both
    the 'list of lines' and 'single string' formats used in .ipynb files."""
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(source)
    return source


def strip_markdown_syntax(text):
    """Remove common Markdown syntax so it doesn't inflate the word count
    (e.g. '#', '*', '`', link brackets, image syntax).

    Code spans (inline `...` and fenced ```...```) are treated as literal
    text: their content is kept, EXCEPT that any image alt-text pattern
    ![alt] inside them is dropped (since "alt text" isn't meaningful prose,
    even when just shown literally as code). A real image outside of code
    -- one that would actually render as a picture -- contributes no words
    at all, so both its alt text and its URL are removed entirely.
    """

    def _strip_alt_only(match):
        # Keep the code content, but drop any "![alt]" image-alt markers
        # inside it (leaving the rest, e.g. the "(url)", intact).
        content = match.group(1)
        return re.sub(r"!\[[^\]]*\]", "", content)

    # Fenced code blocks (```...```): keep content, drop image alt-text within
    text = re.sub(r"```(?:[^\n]*\n)?(.*?)```", _strip_alt_only, text, flags=re.DOTALL)
    # Inline code `like this`: keep content, drop image alt-text within
    text = re.sub(r"`([^`]*)`", _strip_alt_only, text)
    # Remove real images ![alt](url) entirely (alt + url), they render as
    # a picture with no visible text
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    # Remove links [text](url) -> text
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    # Remove heading markers, emphasis markers, blockquote markers
    text = re.sub(r"^[#>\-\*\+]+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_~]{1,3}", "", text)
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    return text


def count_words(text):
    """Count words as whitespace-separated tokens containing at least one
    alphanumeric character."""
    tokens = text.split()
    return sum(1 for t in tokens if re.search(r"\w", t))


def analyze_notebook(path, include_raw=False, strip_markdown=True):
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb.get("cells", [])
    target_types = {"markdown"} | ({"raw"} if include_raw else set())

    total_words = 0
    total_chars = 0
    cell_count = 0
    details = []

    for i, cell in enumerate(cells):
        cell_type = cell.get("cell_type")
        if cell_type not in target_types:
            continue

        raw_text = get_cell_source_text(cell)
        text_for_counting = (
            strip_markdown_syntax(raw_text) if strip_markdown else raw_text
        )

        words = count_words(text_for_counting)
        chars = len(text_for_counting.strip())

        total_words += words
        total_chars += chars
        cell_count += 1
        details.append((i, cell_type, words, chars))

    return {
        "path": str(path),
        "cell_count": cell_count,
        "total_words": total_words,
        "total_chars": total_chars,
        "details": details,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Count words in the text (markdown) cells of a Jupyter notebook."
    )
    parser.add_argument("notebooks", nargs="+", help="Path(s) to .ipynb file(s)")
    parser.add_argument(
        "--include-raw",
        action="store_true",
        help="Also include 'raw' cells in the word count (default: markdown only)",
    )
    parser.add_argument(
        "--keep-markdown-syntax",
        action="store_true",
        help="Don't strip Markdown syntax (#, *, links, etc.) before counting words",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show a per-cell breakdown",
    )
    args = parser.parse_args()

    grand_total_words = 0

    for nb_path in args.notebooks:
        path = Path(nb_path)
        if not path.exists():
            print(f"Error: file not found: {path}", file=sys.stderr)
            continue
        if path.suffix != ".ipynb":
            print(
                f"Warning: {path} does not have an .ipynb extension, skipping.",
                file=sys.stderr,
            )
            continue

        try:
            result = analyze_notebook(
                path,
                include_raw=args.include_raw,
                strip_markdown=not args.keep_markdown_syntax,
            )
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error reading {path}: {e}", file=sys.stderr)
            continue

        grand_total_words += result["total_words"]

        print(f"\n{result['path']}")
        print(f"  Text cells analyzed: {result['cell_count']}")
        print(f"  Total words:         {result['total_words']}")
        print(f"  Total characters:    {result['total_chars']}")

        if args.verbose and result["details"]:
            print("  Per-cell breakdown:")
            for idx, cell_type, words, chars in result["details"]:
                print(
                    f"    Cell {idx:>3} [{cell_type:<8}]  words={words:<5} chars={chars}"
                )

    if len(args.notebooks) > 1:
        print(f"\nGrand total words across all notebooks: {grand_total_words}")


if __name__ == "__main__":
    main()
