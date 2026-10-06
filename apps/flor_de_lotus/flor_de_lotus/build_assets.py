# Copyright (c) 2026, Flor de Lótus and Contributors
# License: GNU General Public License v3. See license.txt

"""Regenera o CSS (e, se pedido, os SVG provisórios) a partir de ``brand.py``."""

from __future__ import annotations

import argparse
from pathlib import Path

from flor_de_lotus.brand import render_logo_svg, render_mark_svg, render_theme_css
from flor_de_lotus.nomenclature import render_translations_csv

PACKAGE = Path(__file__).resolve().parent


def write_generated_files(with_logos: bool = False) -> list[Path]:
	written = [
		_write(PACKAGE / "public" / "css" / "flor_de_lotus.css", render_theme_css()),
		_write(PACKAGE / "translations" / "pt-BR.csv", render_translations_csv()),
	]
	if with_logos:
		images = PACKAGE / "public" / "images"
		written.append(_write(images / "flor-de-lotus-mark-placeholder.svg", render_mark_svg()))
		written.append(_write(images / "flor-de-lotus-logo-placeholder.svg", render_logo_svg()))
	return written


def _write(path: Path, content: str) -> Path:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(content, encoding="utf-8")
	return path


def main() -> None:
	parser = argparse.ArgumentParser(description="Regenera CSS e traduções da Flor de Lótus.")
	parser.add_argument(
		"--with-logos",
		action="store_true",
		help="Reescreve os SVG provisórios. Apaga um logo que tenha sido colocado no lugar deles.",
	)
	args = parser.parse_args()
	for path in write_generated_files(with_logos=args.with_logos):
		print(path)


if __name__ == "__main__":
	main()
