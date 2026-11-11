"""Validate a repository-relative SHA-256 freeze without modifying inputs."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verify(path):
    rows = []
    for line in path.read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        digest, name = line.split('  ', 1)
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Freeze contains an unsafe relative path')
        target = ROOT / relative
        if not target.is_file() or target.is_symlink() or hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError('Frozen input changed: ' + name)
        rows.append(name)
    if not rows or len(rows) != len(set(rows)):
        raise ValueError('Empty or duplicate freeze entries')
    return len(rows)
