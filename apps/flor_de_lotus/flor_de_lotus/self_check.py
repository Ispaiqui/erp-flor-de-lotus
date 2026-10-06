# Copyright (c) 2026, Flor de Lótus and Contributors
# License: GNU General Public License v3. See license.txt

"""Confere a estrutura do app sem precisar de um bench.

    python -m flor_de_lotus.self_check
"""

from __future__ import annotations

import csv
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from flor_de_lotus import brand, hooks, nomenclature
from flor_de_lotus.brand import render_logo_svg, render_mark_svg, render_theme_css

PACKAGE = Path(__file__).resolve().parent
APP_ROOT = PACKAGE.parent


def main() -> None:
	errors: list[str] = []

	def check(condition: bool, message: str) -> None:
		if not condition:
			errors.append(message)

	check(hooks.app_name == "flor_de_lotus", "app_name deve ser flor_de_lotus")
	check(hooks.app_title == "Flor de Lótus", "app_title deve ser Flor de Lótus")
	check(hooks.required_apps == ["erpnext"], "required_apps deve ser ['erpnext']")
	check("General Public License" in hooks.app_license, "a licença do app deve ser a GPL")
	check(hooks.app_color == brand.PALETTE["primary"], "app_color deve sair da PALETTE")
	check(hooks.app_logo_url == brand.LOGO_URL, "app_logo_url deve apontar para o logo provisório")
	check(
		"/assets/flor_de_lotus/css/flor_de_lotus.css" in hooks.app_include_css,
		"o CSS do tema deve entrar no Desk",
	)
	check(
		"/assets/flor_de_lotus/css/flor_de_lotus.css" in hooks.web_include_css,
		"o CSS do tema deve entrar no site e na tela de entrada",
	)
	check(hooks.website_context.get("favicon") == brand.FAVICON_URL, "favicon do site")
	check(hooks.website_context.get("splash_image") == brand.SPLASH_URL, "splash do site")

	css_path = PACKAGE / "public" / "css" / "flor_de_lotus.css"
	css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
	check(css == render_theme_css(), "o CSS em disco divergiu de brand.PALETTE; rode build_assets")
	for name, hex_color in brand.PALETTE.items():
		check(hex_color in css, f"a cor {name} ({hex_color}) não está no CSS")
	check("--fdl-color-primary" in css, "faltam as variáveis --fdl-color-*")

	for filename, renderer in (
		("flor-de-lotus-mark-placeholder.svg", render_mark_svg),
		("flor-de-lotus-logo-placeholder.svg", render_logo_svg),
	):
		path = PACKAGE / "public" / "images" / filename
		text = path.read_text(encoding="utf-8") if path.exists() else ""
		check(path.exists(), f"falta {filename}")
		check("PLACEHOLDER" in text, f"{filename} precisa dizer que é placeholder")
		check(text == renderer(), f"{filename} divergiu da paleta; rode build_assets --with-logos")
		try:
			ET.fromstring(text.encode("utf-8"))
		except ET.ParseError as exc:
			check(False, f"{filename} não é um SVG válido: {exc}")

	csv_path = PACKAGE / "translations" / "pt-BR.csv"
	check(csv_path.exists(), "falta translations/pt-BR.csv")
	rows = list(csv.reader(csv_path.read_text(encoding="utf-8").splitlines()))
	sources = [row[0] for row in rows if row]
	check(len(sources) == len(set(sources)), "há termo original repetido no CSV")
	expected = [(source, translation) for source, translation, _note in nomenclature.TERMS]
	got = [(row[0], row[1]) for row in rows if row]
	check(got == expected, "o CSV não está igual a nomenclature.TERMS")
	check(all(len(row) == 3 for row in rows if row), "cada linha do CSV precisa de 3 colunas")

	glossary = (APP_ROOT / "GLOSSARIO.md").read_text(encoding="utf-8")
	pairs = _glossary_pairs(glossary)
	check(
		pairs == expected,
		"a tabela do glossário não lista os mesmos termos, na mesma ordem, que nomenclature.TERMS",
	)
	for needle in ("Depósito", "Nota de venda", "PDV", "Caixa", "provisória", "GPL-3.0"):
		check(needle in glossary, f"o glossário deveria mencionar {needle}")

	readme = (APP_ROOT / "README.md").read_text(encoding="utf-8")
	for needle in (
		"bench",
		"install-app flor_de_lotus",
		"brand.py",
		"PLACEHOLDER",
		"pt-BR",
		"GPL",
		"apps/flor_de_lotus",
	):
		check(needle in readme, f"o README deveria mencionar {needle}")

	check((APP_ROOT / "license.txt").read_text(encoding="utf-8").startswith("                    GNU GENERAL PUBLIC LICENSE"), "license.txt não é a GPL-3.0")
	check((APP_ROOT / "pyproject.toml").read_text(encoding="utf-8").startswith("[project]\nname = \"flor_de_lotus\""), "pyproject")
	check((PACKAGE / "modules.txt").read_text(encoding="utf-8").strip() == "Flor de Lotus", "modules.txt")
	check((PACKAGE / "flor_de_lotus" / "__init__.py").exists(), "pasta do módulo Flor de Lotus")
	check((PACKAGE / "patches.txt").exists(), "patches.txt")

	# Importar os módulos que o bench vai carregar, sem subir o Frappe.
	import flor_de_lotus.boot  # noqa: F401
	import flor_de_lotus.install  # noqa: F401
	import flor_de_lotus.permissions  # noqa: F401

	check(flor_de_lotus.install._as_bool("true") is True, "overwrite true")
	check(flor_de_lotus.install._as_bool("false") is False, "overwrite false")
	check(flor_de_lotus.install._as_bool(False) is False, "overwrite bool false")
	check(
		flor_de_lotus.boot.language_for_guest("pt-BR", "", "") == "pt-BR",
		"visitante sem escolha usa o idioma do site",
	)
	check(
		flor_de_lotus.boot.language_for_guest("pt-BR", "en", "") is None,
		"visitante com _lang explícito não é forçado",
	)
	check(
		flor_de_lotus.boot.language_for_guest("pt-BR", "", "en") is None,
		"visitante com cookie de idioma não é forçado",
	)

	if errors:
		print("\n".join(errors), file=sys.stderr)
		raise SystemExit(1)
	print(f"ok: {len(nomenclature.TERMS)} termos, tema e estrutura do app flor_de_lotus")


def _glossary_pairs(text: str) -> list[tuple[str, str]]:
	pairs: list[tuple[str, str]] = []
	for line in text.splitlines():
		if not line.startswith("|"):
			continue
		cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
		if len(cells) < 2:
			continue
		if cells[0] in {"Termo na operação", "---"} or set(cells[0]) <= {"-", ":"}:
			continue
		if cells[1].startswith("---"):
			continue
		pairs.append((cells[1], cells[0]))
	return pairs


if __name__ == "__main__":
	main()
