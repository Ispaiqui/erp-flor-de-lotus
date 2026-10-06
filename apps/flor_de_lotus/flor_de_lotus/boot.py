# Copyright (c) 2026, Flor de Lótus and Contributors
# License: GNU General Public License v3. See license.txt

"""Aplica a marca na sessão e no site sem gravar por cima de um logo já trocado."""

from __future__ import annotations

from flor_de_lotus.brand import (
	APP_TITLE,
	DEFAULT_APP_NAMES,
	DEFAULT_FAVICON_URLS,
	DEFAULT_LOGO_URLS,
	FAVICON_URL,
	LOGO_URL,
	SPLASH_URL,
)


def extend_bootinfo(bootinfo):
	"""Roda no boot do Desk e também como ``boot_session``.

	O Frappe, quando há mais de dois apps, não escolhe sozinho o logo do
	último app. Se o logo da sessão ainda for o do Frappe ou do ERPNext,
	trocamos pelo placeholder. Um arquivo que o dono já tenha definido
	fica como está.
	"""
	current = getattr(bootinfo, "app_logo_url", None)
	if current in DEFAULT_LOGO_URLS or not current:
		bootinfo.app_logo_url = LOGO_URL

	sysdefaults = getattr(bootinfo, "sysdefaults", None)
	if sysdefaults is None or not hasattr(sysdefaults, "get"):
		return
	if sysdefaults.get("app_name") in DEFAULT_APP_NAMES:
		sysdefaults.app_name = APP_TITLE


def update_website_context(context):
	"""Favicon, splash e nome na página de entrada, se ainda forem os padrões."""
	_prefer(context, "favicon", FAVICON_URL, DEFAULT_FAVICON_URLS)
	_prefer(context, "splash_image", SPLASH_URL, DEFAULT_LOGO_URLS)
	_prefer(context, "logo", LOGO_URL, DEFAULT_LOGO_URLS)
	if context.get("app_name") in DEFAULT_APP_NAMES:
		context["app_name"] = APP_TITLE


def _prefer(context, key: str, value: str, defaults: frozenset) -> None:
	current = context.get(key)
	if current in defaults or not current:
		context[key] = value


def language_for_guest(site_language: str | None, explicit: str | None, cookie: str | None) -> str | None:
	"""Idioma da tela de entrada.

	O Frappe, para quem não entrou, usa o idioma do navegador antes do
	idioma do site. Um Chrome em inglês abre a marca em inglês mesmo com
	o site em pt-BR. Se a pessoa não escolheu um idioma (cookie ou
	``?_lang``), vale o idioma do site.
	"""
	if (explicit or "").strip() or (cookie or "").strip():
		return None
	return (site_language or "").strip() or None


def use_site_language_for_guests() -> None:
	import frappe

	if getattr(getattr(frappe, "session", None), "user", None) != "Guest":
		return
	request = getattr(frappe, "request", None)
	cookie = ""
	if request is not None:
		cookie = request.cookies.get("preferred_language") or ""
	explicit = ""
	form = getattr(frappe, "form_dict", None)
	if form is not None:
		explicit = form.get("_lang") or ""
	chosen = language_for_guest(frappe.get_system_settings("language"), explicit, cookie)
	if chosen:
		frappe.local.lang = chosen
