# Copyright (c) 2026, Flor de Lótus and Contributors
# License: GNU General Public License v3. See license.txt

"""Regras de loja no servidor.

O menu esconde o que dá. Quem chama a API continua limitado aqui:
permissão do DocType, User Permission e estas checagens.

Adaptação da V1: a User Permission de depósito e de centro de custo vale
só para o próprio documento (applicable_for). Se valesse para todo
vínculo, a empresa sumiria, porque a empresa aponta para o depósito
padrão. A permissão de Loja e de perfil de PDV vale para todos os
vínculos, e é isso que limita funcionário, usuário e sessão de caixa.
"""

from __future__ import annotations

ROLE_DONO = "Dono"
ROLE_GERENTE = "Gerente da loja"
ROLE_CAIXA = "Caixa"
ROLE_ESTOQUISTA = "Estoquista"
ROLE_FABRICACAO = "Fabricação"

STORE_SCOPED_ROLES = frozenset({ROLE_GERENTE, ROLE_CAIXA})
BROAD_ITEM_ROLES = frozenset(
	{
		ROLE_DONO,
		ROLE_GERENTE,
		ROLE_CAIXA,
		ROLE_ESTOQUISTA,
		"System Manager",
		"Administrator",
		"Item Manager",
		"Stock Manager",
		"Stock User",
		"Sales User",
		"Sales Manager",
	}
)
BLOCKED_ASSIGN_ROLES = frozenset({"Dono", "System Manager", "Administrator"})
POS_DOCTYPES = ("POS Invoice", "POS Opening Entry", "POS Closing Entry")


def validate_user(doc, method=None):
	import frappe

	if not _column("User", "loja"):
		return
	actor = frappe.session.user
	if not _is_gerente_only(actor):
		return

	allowed = _lojas_of(actor)
	if not allowed or doc.loja not in allowed:
		frappe.throw("O gerente só grava usuários da própria loja.")

	roles = {row.role for row in doc.roles or []}
	for profile in doc.role_profiles or []:
		if not profile.role_profile:
			continue
		roles.update(
			frappe.get_all("Has Role", filters={"parent": profile.role_profile, "parenttype": "Role Profile"}, pluck="role")
		)
	if roles & BLOCKED_ASSIGN_ROLES:
		frappe.throw("O gerente não pode atribuir a função Dono nem administrador.")


def validate_employee(doc, method=None):
	import frappe

	if not _column("Employee", "loja"):
		return
	actor = frappe.session.user
	if not _is_gerente_only(actor):
		return

	allowed = _lojas_of(actor)
	if not allowed or doc.loja not in allowed:
		frappe.throw("O gerente só grava funcionários da própria loja.")


def sync_user_permissions(doc, method=None):
	if not _column("User", "loja"):
		return
	_sync(doc.name)


def sync_loja_links(doc, method=None):
	import frappe

	if not _column("User", "loja"):
		return

	users = set(frappe.get_all("User", filters={"loja": doc.name}, pluck="name"))
	if doc.gerente:
		users.add(doc.gerente)
		if not frappe.db.get_value("User", doc.gerente, "loja"):
			frappe.db.set_value("User", doc.gerente, "loja", doc.name, update_modified=False)
	for user in users:
		_sync(user)


def loja_query(user=None):
	return _scoped_name_query("Loja", user)


def employee_query(user=None):
	if not _column("Employee", "loja"):
		return ""
	user = _user(user)
	if _unrestricted(user) or not _is_gerente_only(user):
		return ""
	return _in_clause("Employee", "loja", _lojas_of(user))


def user_query(user=None):
	import frappe

	if not _column("User", "loja"):
		return ""
	user = _user(user)
	if _unrestricted(user) or not _is_gerente_only(user):
		return ""
	lojas = _lojas_of(user)
	if not lojas:
		return f"`tabUser`.`name` = {frappe.db.escape(user)}"
	values = ", ".join(frappe.db.escape(value) for value in lojas)
	return f"(`tabUser`.`name` = {frappe.db.escape(user)} or `tabUser`.`loja` in ({values}))"


def item_query(user=None):
	if not _column("Item", "catalogo"):
		return ""
	user = _user(user)
	if not _vela_only(user):
		return ""
	return "`tabItem`.`catalogo` = 'Vela'"


def pos_invoice_query(user=None):
	return _pos_query("POS Invoice", user)


def pos_opening_query(user=None):
	return _pos_query("POS Opening Entry", user)


def pos_closing_query(user=None):
	return _pos_query("POS Closing Entry", user)


def loja_has_permission(doc, ptype=None, user=None, debug=False):
	user = _user(user)
	if _unrestricted(user) or not _store_scoped(user):
		return True
	return bool(doc and doc.name in _lojas_of(user))


def employee_has_permission(doc, ptype=None, user=None, debug=False):
	if not _column("Employee", "loja"):
		return True
	user = _user(user)
	if _unrestricted(user) or not _is_gerente_only(user):
		return True
	return bool(doc and doc.loja in _lojas_of(user))


def user_has_permission(doc, ptype=None, user=None, debug=False):
	if not _column("User", "loja"):
		return True
	user = _user(user)
	if _unrestricted(user) or not _is_gerente_only(user):
		return True
	if not doc or doc.name == user:
		return True
	return bool(doc.loja in _lojas_of(user))


def item_has_permission(doc, ptype=None, user=None, debug=False):
	if not _column("Item", "catalogo"):
		return True
	user = _user(user)
	if not _vela_only(user):
		return True
	return bool(doc and doc.catalogo == "Vela")


def pos_has_permission(doc, ptype=None, user=None, debug=False):
	user = _user(user)
	if _unrestricted(user):
		return True
	roles = _roles(user)
	if roles & {ROLE_ESTOQUISTA, ROLE_FABRICACAO} and not (roles & STORE_SCOPED_ROLES):
		return False
	if not (roles & STORE_SCOPED_ROLES):
		return True
	allowed = _user_permission_values(user, "POS Profile")
	profile = getattr(doc, "pos_profile", None) if doc else None
	return bool(profile and profile in allowed)


def _sync(user: str) -> None:
	import frappe
	from frappe.permissions import add_user_permission

	if user in {"Administrator", "Guest"} or not frappe.db.exists("User", user):
		return

	loja_name = frappe.db.get_value("User", user, "loja")
	store_warehouses = set(frappe.get_all("Loja", pluck="deposito"))
	store_cost_centers = set(frappe.get_all("Loja", pluck="centro_de_custo"))
	store_profiles = set(frappe.get_all("Loja", pluck="perfil_de_pdv"))

	_delete_permissions(user, "Loja")
	_delete_permissions(user, "Warehouse", store_warehouses)
	_delete_permissions(user, "Cost Center", store_cost_centers)
	_delete_permissions(user, "POS Profile", store_profiles)

	if not loja_name or not frappe.db.exists("Loja", loja_name):
		return

	loja = frappe.get_doc("Loja", loja_name)
	add_user_permission("Loja", loja.name, user, ignore_permissions=True)
	if loja.deposito:
		add_user_permission(
			"Warehouse", loja.deposito, user, ignore_permissions=True, applicable_for="Warehouse"
		)
	if loja.centro_de_custo:
		add_user_permission(
			"Cost Center",
			loja.centro_de_custo,
			user,
			ignore_permissions=True,
			applicable_for="Cost Center",
		)
	if loja.perfil_de_pdv:
		add_user_permission("POS Profile", loja.perfil_de_pdv, user, ignore_permissions=True)


def _delete_permissions(user: str, doctype: str, only_values: set | None = None) -> None:
	import frappe

	filters = {"user": user, "allow": doctype}
	for row in frappe.get_all("User Permission", filters=filters, fields=["name", "for_value"]):
		if only_values is not None and row.for_value not in only_values:
			continue
		frappe.delete_doc("User Permission", row.name, ignore_permissions=True, force=True)


def _pos_query(doctype: str, user: str | None) -> str:
	if not _column(doctype, "pos_profile"):
		return ""
	user = _user(user)
	if _unrestricted(user):
		return ""
	roles = _roles(user)
	if roles & {ROLE_ESTOQUISTA, ROLE_FABRICACAO} and not (roles & STORE_SCOPED_ROLES):
		return "1=0"
	if not (roles & STORE_SCOPED_ROLES):
		return ""
	return _in_clause(doctype, "pos_profile", _user_permission_values(user, "POS Profile"))


def _scoped_name_query(doctype: str, user: str | None) -> str:
	user = _user(user)
	if _unrestricted(user) or not _store_scoped(user):
		return ""
	return _in_clause(doctype, "name", _lojas_of(user))


def _in_clause(doctype: str, field: str, values: list[str]) -> str:
	import frappe

	if not values:
		return "1=0"
	joined = ", ".join(frappe.db.escape(value) for value in values)
	return f"`tab{doctype}`.`{field}` in ({joined})"


def _lojas_of(user: str) -> list[str]:
	import frappe

	if not _column("User", "loja"):
		return []
	loja = frappe.db.get_value("User", user, "loja")
	return [loja] if loja else []


def _user_permission_values(user: str, doctype: str) -> list[str]:
	import frappe

	return frappe.get_all("User Permission", filters={"user": user, "allow": doctype}, pluck="for_value")


def _vela_only(user: str) -> bool:
	roles = _roles(user)
	return ROLE_FABRICACAO in roles and not (roles & BROAD_ITEM_ROLES)


def _store_scoped(user: str) -> bool:
	return bool(_roles(user) & STORE_SCOPED_ROLES) and not _unrestricted(user)


def _is_gerente_only(user: str) -> bool:
	if _unrestricted(user):
		return False
	return ROLE_GERENTE in _roles(user)


def _unrestricted(user: str) -> bool:
	if user in {"Administrator", "Guest"}:
		return user == "Administrator"
	return bool(_roles(user) & {"System Manager", ROLE_DONO})


def _roles(user: str) -> set[str]:
	import frappe

	return set(frappe.get_roles(user))


def _user(user: str | None) -> str:
	import frappe

	return user or frappe.session.user


def _column(doctype: str, fieldname: str) -> bool:
	import frappe

	try:
		return bool(frappe.db.has_column(doctype, fieldname))
	except Exception:
		return False
