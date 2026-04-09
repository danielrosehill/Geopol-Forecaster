"""Shell out to the Typst CLI to render PDF.

Requires `typst` binary on PATH. On Ubuntu: `snap install typst` or grab the
binary from https://github.com/typst/typst/releases.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class TypstNotInstalled(RuntimeError):
    pass


def render_pdf(typst_source: str, out_dir: Path, basename: str = "report") -> Path:
    if not shutil.which("typst"):
        raise TypstNotInstalled(
            "`typst` binary not found on PATH. Install from https://typst.app/"
        )
    out_dir.mkdir(parents=True, exist_ok=True)
    src_path = out_dir / f"{basename}.typ"
    pdf_path = out_dir / f"{basename}.pdf"
    src_path.write_text(typst_source, encoding="utf-8")
    subprocess.run(
        ["typst", "compile", str(src_path), str(pdf_path)],
        check=True,
    )
    return pdf_path
