#!/usr/bin/env python3
import re
import sys
from pathlib import Path
import json

# Simple LaTeX -> text extractor and basic similarity metrics (shingles)
# Note: This is a heuristic cleaner to prepare text for external plagiarism tools.

SECTION_CMDS = [
    'part', 'chapter', 'section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph'
]

# Patterns to keep content
KEEP_BLOCK_PATTERNS = [
    (re.compile(r"\\caption\s*\{([^}]*)\}", re.DOTALL), lambda m: f"Caption: {m.group(1)}\n"),
]

# Patterns to convert sections
SECTION_PATTERNS = [
    (re.compile(rf"\\{cmd}\\*?\s*\{{([^}}]*)\}}", re.DOTALL), cmd.upper()) for cmd in SECTION_CMDS
]

# Remove environments markers
BEGIN_END_RE = re.compile(r"\\(begin|end)\s*\{[^}]*\}")

# Remove citations/labels/refs/footnotes (keep minimal hint)
SIMPLE_REMOVE = [
    re.compile(r"\\label\s*\{[^}]*\}"),
    re.compile(r"\\ref\s*\{[^}]*\}"),
    re.compile(r"\\pageref\s*\{[^}]*\}"),
    re.compile(r"\\cite[t|p|alt|alp|year|author|]{0,10}\s*\{[^}]*\}"),
]

# Footnotes -> [nota]
FOOTNOTE_RE = re.compile(r"\\footnote\s*\{([^}]*)\}", re.DOTALL)

# Math removal/conversion
INLINE_MATH = re.compile(r"\$(.*?)\$", re.DOTALL)
DISPLAY_MATH = re.compile(r"\\\[(.*?)\\\]", re.DOTALL)
PARENS_DISPLAY = re.compile(r"\n\s*\\\((.*?)\\\)\s*\n", re.DOTALL)

# Generic command with one arg: \cmd{...} -> content or nothing
CMD_ONEARG = re.compile(r"\\[a-zA-Z@]+\s*\{([^}]*)\}")
# Generic command no-arg: \cmd or \cmd[...]
CMD = re.compile(r"\\[a-zA-Z@]+(\[[^\]]*\])?")

# Braces cleanup
BRACES = re.compile(r"[{}]")

# Multiple spaces
MULTISPACE = re.compile(r"\s{2,}")


def latex_to_text(tex: str) -> str:
    s = tex
    # Normalize newlines
    s = s.replace('\r\n', '\n').replace('\r', '\n')

    # Keep captions
    for pat, repl in KEEP_BLOCK_PATTERNS:
        s = pat.sub(repl, s)

    # Convert sections
    for pat, name in SECTION_PATTERNS:
        s = pat.sub(lambda m: f"\n\n{name}: {m.group(1)}\n\n", s)

    # Remove begin/end markers
    s = BEGIN_END_RE.sub('\n', s)

    # Remove simple refs/cites/labels
    for pat in SIMPLE_REMOVE:
        s = pat.sub('', s)

    # Footnotes -> inlined in brackets
    s = FOOTNOTE_RE.sub(lambda m: f" [nota: {m.group(1).strip()}] ", s)

    # Remove display and inline math (keep plain content lightly)
    s = DISPLAY_MATH.sub(lambda m: ' ' + re.sub(CMD, '', m.group(1)), s)
    s = PARENS_DISPLAY.sub(lambda m: ' ' + re.sub(CMD, '', m.group(1)) + ' ', s)
    s = INLINE_MATH.sub(lambda m: ' ' + re.sub(CMD, '', m.group(1)) + ' ', s)

    # Remove generic LaTeX commands with one arg -> keep arg content
    s = CMD_ONEARG.sub(lambda m: ' ' + m.group(1) + ' ', s)

    # Remove remaining commands
    s = CMD.sub(' ', s)

    # Remove braces
    s = BRACES.sub(' ', s)

    # Remove TeX comments (line-based)
    s = '\n'.join(line.split('%', 1)[0] for line in s.splitlines())

    # Collapse whitespace
    s = MULTISPACE.sub(' ', s)
    s = re.sub(r"\s*\n\s*", '\n', s)

    # Trim
    return s.strip()


def shingles(words, n=5):
    return {' '.join(words[i:i+n]) for i in range(0, max(0, len(words)-n+1))}


def main():
    if len(sys.argv) > 1:
        tex_path = Path(sys.argv[1])
    else:
        tex_path = Path(__file__).resolve().parents[1] / 'Practica.tex'

    if not tex_path.exists():
        print(f"Input not found: {tex_path}", file=sys.stderr)
        sys.exit(1)

    raw = tex_path.read_text(encoding='utf-8', errors='ignore')
    text = latex_to_text(raw)

    out_txt = tex_path.with_name(tex_path.stem + '_plain.txt')
    out_json = tex_path.with_name(tex_path.stem + '_similarity_report.json')

    out_txt.write_text(text, encoding='utf-8')

    # Basic metrics
    chars = len(text)
    words = re.findall(r"\w+", text, flags=re.UNICODE)
    word_count = len(words)
    sent_count = len(re.findall(r"[\.!?]", text))

    sh3 = shingles(words, 3)
    sh5 = shingles(words, 5)

    report = {
        'file': str(tex_path),
        'output_text': str(out_txt),
        'characters': chars,
        'words': word_count,
        'sentences_est': sent_count,
        'unique_3gram_shingles': len(sh3),
        'unique_5gram_shingles': len(sh5),
        'note': 'Este informe NO es Turnitin. Son métricas locales para preparar un chequeo externo.'
    }

    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
