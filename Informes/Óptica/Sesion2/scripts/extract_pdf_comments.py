#!/usr/bin/env python3
from pathlib import Path
import json
import sys
from pypdf import PdfReader

# Extract text annotations (sticky notes, highlights w/comments) from a PDF.
# Output: JSON to stdout and write a sidecar .comments.json next to the PDF.

def extract_comments(pdf_path: Path):
    reader = PdfReader(str(pdf_path))
    comments = []
    for i, page in enumerate(reader.pages, start=1):
        annots = page.get("/Annots", [])
        if not annots:
            continue
        for a in annots:
            obj = a.get_object()
            subtype = obj.get("/Subtype")
            contents = obj.get("/Contents")
            author = obj.get("/T")
            # Highlight may store rich content differently; try both
            if contents is None and obj.get("/RC") is not None:
                contents = obj.get("/RC")
            if contents is None:
                continue
            comments.append({
                "page": i,
                "type": str(subtype) if subtype else None,
                "author": str(author) if author else None,
                "text": str(contents).strip(),
            })
    return comments


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_pdf_comments.py <file.pdf>", file=sys.stderr)
        sys.exit(2)
    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)
    comments = extract_comments(pdf_path)
    sidecar = pdf_path.with_suffix('.comments.json')
    sidecar.write_text(json.dumps(comments, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({
        "file": str(pdf_path),
        "count": len(comments),
        "output": str(sidecar)
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
