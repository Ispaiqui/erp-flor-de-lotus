# Copyright (c) 2026, Flor de Lótus and Contributors
# License: GNU General Public License v3. See license.txt

"""Grava a marca nos ajustes do site na instalação.

O Frappe lê o logo da tela de entrada em Website Settings e Navbar
Settings antes de olhar o gancho ``app_logo_url``. Sem este passo, com
Frappe + ERPNext + este app, a tela pode continuar com o logo do Frappe.

Não sobrescreve um valor que o dono já tenha trocado. Para repor os
placeholders:

    bench --site SEU_SITE execute flor_de_lotus.install.apply_branding --kwargs "{'overwrite': True}"

O valor de ``--kwargs`` é avaliado como código Python (``eval``), não como JSON.
``{"overwrite": true}`` falha com ``NameError`` porque ``true`` não existe no Python.
"""

from __future__ import annotations

from flor_de_lotus.brand import (
	APP_TITLE,
	BRAND_HTML,
	DEFAULT_APP_NAMES,
	DEFAULT_FAVICON_URLS,
	DEFAULT_LOGO_URLS,
	FAVICON_URL,
	LOGO_URL,
	SPLASH_URL,
)


def after_install():
	apply_branding(overwrite=False)
	_set_language_if_english()


def after_migrate():
	# Migrações seguintes só preenchem o que ainda estiver no padrão.
	# Idioma não entra aqui: se o dono voltar para inglês, a migração
	# não desfaz essa escolha.
	apply_branding(overwrite=False)
	# Import tardio: este módulo não puxa o Frappe na conferência do app.
	from flor_de_lotus.setup_v1 import seed_v1

	seed_v1()


def apply_branding(overwrite: bool = False) -> list[str]:
	"""Aponta nome, logo, favicon e splash para a marca provisória."""
	import frappe

	overwrite = _as_bool(overwrite)
	changed: list[str] = []
	specs = (
		("System Settings", "app_name", APP_TITLE, DEFAULT_APP_NAMES),
		("Website Settings", "app_name", APP_TITLE, DEFAULT_APP_NAMES),
		("Website Settings", "title_prefix", APP_TITLE, DEFAULT_APP_NAMES),
		("Website Settings", "app_logo", LOGO_URL, DEFAULT_LOGO_URLS),
		("Website Settings", "splash_image", SPLASH_URL, DEFAULT_LOGO_URLS),
		("Website Settings", "favicon", FAVICON_URL, DEFAULT_FAVICON_URLS),
		("Website Settings", "brand_html", BRAND_HTML, frozenset({None, ""})),
		("Website Settings", "footer_powered", APP_TITLE, frozenset({None, ""})),
		("Navbar Settings", "app_logo", LOGO_URL, DEFAULT_LOGO_URLS),
	)
	for doctype, fieldname, value, defaults in specs:
		if _set_if_default(doctype, fieldname, value, defaults, overwrite):
			changed.append(f"{doctype}.{fieldname}")

	frappe.clear_cache()
	return changed


def _set_language_if_english() -> None:
	import frappe

	try:
		current = frappe.db.get_single_value("System Settings", "language")
	except Exception:
		frappe.logger("flor_de_lotus").warning("Não foi possível ler o idioma do site.", exc_info=True)
		return

	if current not in (None, "", "en"):
		return
	if not frappe.db.exists("Language", "pt-BR"):
		frappe.logger("flor_de_lotus").warning(
			"Idioma pt-BR não está cadastrado. Defina Português (Brasil) em System Settings."
		)
		return
	frappe.db.set_single_value("System Settings", "language", "pt-BR")


def _as_bool(value) -> bool:
	if isinstance(value, str):
		return value.strip().lower() in {"1", "true", "yes", "sim"}
	return bool(value)


def _set_if_default(doctype: str, fieldname: str, value: str, defaults: frozenset, overwrite: bool) -> bool:
	import frappe

	try:
		current = frappe.db.get_single_value(doctype, fieldname)
	except Exception:
		frappe.logger("flor_de_lotus").warning(
			"Não foi possível ler %s.%s para aplicar a marca.", doctype, fieldname, exc_info=True
		)
		return False

	if current == value:
		return False
	if not overwrite and current not in defaults:
		return False

	frappe.db.set_single_value(doctype, fieldname, value)
	return True
