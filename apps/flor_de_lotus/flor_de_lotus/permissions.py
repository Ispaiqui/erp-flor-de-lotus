# Copyright (c) 2026, Flor de Lótus and Contributors
# License: GNU General Public License v3. See license.txt


def check_app_permission() -> bool:
	"""Quem usa o Desk pode abrir o app. Visitante do site, não."""
	import frappe

	if getattr(frappe.session, "user", None) == "Administrator":
		return True

	data = getattr(frappe.session, "data", None)
	user_type = data.get("user_type") if data is not None and hasattr(data, "get") else None
	return user_type != "Website User"
