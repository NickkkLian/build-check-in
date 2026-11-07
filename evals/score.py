"""Shared unchanged parsing helpers from the earlier evaluation."""
import json
import re

HEADING = re.compile(r"(?m)^(?:#{1,6}[ \t]+(?P<hash>[^\n]+?)|\*\*(?P<bold>[^*\n]+?)\*\*:?)[ \t]*$")


def sections(text):
    """(title, body) pairs. Markdown headings and stand-alone bold lines both open a section."""
    marks = list(HEADING.finditer(text))
    pairs = [("", text[:marks[0].start()] if marks else text)]
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        pairs.append((mark.group("hash") or mark.group("bold") or "", text[mark.end():end].lstrip("\n")))
    return pairs


def envelope_denials(target):
    path = target / "envelope.json"
    if not path.is_file():
        return []
    try:
        envelope = json.loads(path.read_text())
    except json.JSONDecodeError:
        return ["unreadable envelope"]
    return [d.get("tool_input", {}).get("file_path", d.get("tool_name", "?")) if isinstance(d, dict) else str(d) for d in envelope.get("permission_denials") or []]


