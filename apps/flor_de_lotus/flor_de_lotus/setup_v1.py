# Copyright (c) 2026, Flor de Lótus and Contributors
# License: GNU General Public License v3. See license.txt

"""Dados da V1, reaplicáveis a cada migração.

Sem a empresa Flor de Lótus (o assistente de instalação ainda não rodou),
as funções e os quadros são criados e a carga de demonstração espera.
A migração seguinte completa lojas, produtos e usuários.

Escolhas desta carga, enquanto o dono não fecha o resto:

- uma empresa, uma lista de preço para as cinco lojas;
- perfil de PDV só com dinheiro e conta de abatimento, para o vínculo existir
  (a grade de venda é da V4);
- depósito e centro de custo na User Permission limitados ao próprio
  documento, para a empresa continuar visível;
- o depósito "Lojas" que o ERPNext cria vira o grupo das lojas, e o
  depósito padrão da empresa passa a ser o Central;
- quadros criados aqui, e não em JSON, porque as funções nascem na migração.
"""

from __future__ import annotations

import json

from flor_de_lotus.access import (
	ROLE_CAIXA,
	ROLE_DONO,
	ROLE_ESTOQUISTA,
	ROLE_FABRICACAO,
	ROLE_GERENTE,
)
from flor_de_lotus.brand import PALETTE

COMPANY_NAME = "Flor de Lótus"
DEMO_PASSWORD = "FlorDemo2026"
PRICE_LIST_NAME = "Varejo Flor de Lótus"
CUSTOMER_NAME = "Consumidor não identificado"
MODULE = "Flor de Lotus"

WS_DONO = "Dono"
WS_GERENTE = "Gerente da loja"
WS_CAIXA = "Caixa"

LOJA_NAMES = tuple(f"Flor de Lótus Loja {index}" for index in range(1, 6))

DEMO_USERS = (
	{
		"email": "dono@flor.localhost",
		"first_name": "Helena",
		"profile": ROLE_DONO,
		"loja_index": None,
		"workspace": WS_DONO,
		"gender": "Female",
	},
	{
		"email": "gerente.loja1@flor.localhost",
		"first_name": "Marina",
		"profile": ROLE_GERENTE,
		"loja_index": 1,
		"workspace": WS_GERENTE,
		"gender": "Female",
	},
	{
		"email": "gerente.loja2@flor.localhost",
		"first_name": "Beatriz",
		"profile": ROLE_GERENTE,
		"loja_index": 2,
		"workspace": WS_GERENTE,
		"gender": "Female",
	},
	{
		"email": "caixa.loja1@flor.localhost",
		"first_name": "Ana",
		"profile": ROLE_CAIXA,
		"loja_index": 1,
		"workspace": WS_CAIXA,
		"gender": "Female",
	},
	{
		"email": "caixa.loja2@flor.localhost",
		"first_name": "Camila",
		"profile": ROLE_CAIXA,
		"loja_index": 2,
		"workspace": WS_CAIXA,
		"gender": "Female",
	},
	{
		"email": "estoquista@flor.localhost",
		"first_name": "Pedro",
		"profile": ROLE_ESTOQUISTA,
		"loja_index": None,
		"workspace": None,
		"gender": "Male",
	},
	{
		"email": "fabricacao@flor.localhost",
		"first_name": "Lúcia",
		"profile": ROLE_FABRICACAO,
		"loja_index": None,
		"workspace": None,
		"gender": "Female",
	},
)

# código, nome, grupo, preço, catálogo
PRODUCTS = (
	("FDL-001", "Vela de soja Lavanda", "Velas", 48, "Produto"),
	("FDL-002", "Vela de soja Baunilha", "Velas", 46, "Produto"),
	("FDL-003", "Vela aromática Flor de lótus", "Velas", 52, "Produto"),
	("FDL-004", "Kit presente três velas", "Presentes", 129, "Produto"),
	("FDL-005", "Difusor de ambientes Chá branco", "Casa e decoração", 68, "Produto"),
	("FDL-006", "Sabonete artesanal Mel", "Casa e decoração", 22, "Produto"),
	("FDL-007", "Caixa presente linho", "Presentes", 35, "Produto"),
	("FDL-008", "Incenso de palo santo", "Casa e decoração", 28, "Produto"),
	("FDL-009", "Porta-vela de cerâmica", "Casa e decoração", 54, "Produto"),
	("FDL-010", "Bandeja de madeira", "Casa e decoração", 79, "Produto"),
	("FDL-011", "Cartão presente Flor de Lótus", "Presentes", 8, "Produto"),
	("FDL-012", "Vela copo Âmbar", "Velas", 39, "Produto"),
	("FDL-013", "Spray de ambiente Folha de figo", "Casa e decoração", 42, "Produto"),
	("FDL-014", "Sachê perfumado Lavanda", "Casa e decoração", 18, "Produto"),
	("FDL-015", "Vela pilar Branca", "Velas", 64, "Produto"),
	("FDL-016", "Cera de soja a granel", "Insumos de vela", 36, "Vela"),
	("FDL-017", "Pavio de algodão", "Insumos de vela", 6, "Vela"),
	("FDL-018", "Essência lavanda", "Insumos de vela", 24, "Vela"),
)

READ = {"read": 1, "select": 1, "report": 1, "print": 1, "export": 1}
FULL = {**READ, "write": 1, "create": 1, "delete": 1, "email": 1, "share": 1}
SUBMIT = {**FULL, "submit": 1, "cancel": 1, "amend": 1}

ROLE_PERMS = {
	"Item": {
		ROLE_DONO: FULL,
		ROLE_GERENTE: READ,
		ROLE_CAIXA: READ,
		ROLE_ESTOQUISTA: READ,
		ROLE_FABRICACAO: READ,
	},
	"Item Group": {
		ROLE_DONO: FULL,
		ROLE_GERENTE: READ,
		ROLE_CAIXA: READ,
		ROLE_ESTOQUISTA: READ,
		ROLE_FABRICACAO: READ,
	},
	"Item Price": {
		ROLE_DONO: FULL,
		ROLE_GERENTE: READ,
		ROLE_CAIXA: READ,
	},
	"Price List": {
		ROLE_DONO: FULL,
		ROLE_GERENTE: READ,
		ROLE_CAIXA: READ,
	},
	"Employee": {
		ROLE_DONO: FULL,
		ROLE_GERENTE: FULL,
	},
	"User": {
		ROLE_DONO: FULL,
		ROLE_GERENTE: {**READ, "write": 1, "create": 1, "email": 1},
	},
	"Warehouse": {
		ROLE_DONO: {**READ, "write": 1, "create": 1},
		ROLE_GERENTE: READ,
		ROLE_CAIXA: READ,
		ROLE_ESTOQUISTA: READ,
		ROLE_FABRICACAO: READ,
	},
	"Cost Center": {
		ROLE_DONO: READ,
		ROLE_GERENTE: READ,
		ROLE_CAIXA: READ,
		ROLE_ESTOQUISTA: READ,
		ROLE_FABRICACAO: READ,
	},
	"POS Profile": {
		ROLE_DONO: {**READ, "write": 1, "create": 1},
		ROLE_GERENTE: READ,
		ROLE_CAIXA: READ,
	},
	"POS Opening Entry": {
		ROLE_DONO: SUBMIT,
		ROLE_GERENTE: SUBMIT,
		ROLE_CAIXA: SUBMIT,
	},
	"POS Closing Entry": {
		ROLE_DONO: SUBMIT,
		ROLE_GERENTE: SUBMIT,
		ROLE_CAIXA: SUBMIT,
	},
	"POS Invoice": {
		ROLE_DONO: READ,
		ROLE_GERENTE: READ,
		ROLE_CAIXA: READ,
	},
	"Company": {
		ROLE_DONO: READ,
		ROLE_GERENTE: READ,
		ROLE_CAIXA: READ,
		ROLE_ESTOQUISTA: READ,
		ROLE_FABRICACAO: READ,
	},
}


def seed_v1() -> None:
	import frappe

	frappe.flags.mute_emails = True
	_ensure_roles()
	_ensure_role_profiles()
	_ensure_custom_fields()
	frappe.clear_cache()
	_ensure_docperms()
	_ensure_workspaces()

	company = _company()
	if not company:
		frappe.logger("flor_de_lotus").warning(
			"V1: empresa %s ainda não existe. Funções e quadros foram criados; "
			"lojas, produtos e usuários de demonstração entram na próxima migração.",
			COMPANY_NAME,
		)
		return

	warehouses = _seed_warehouses(company)
	cost_centers = _seed_cost_centers(company)
	_seed_catalog(company)
	_ensure_customer(company)
	for spec in DEMO_USERS:
		_ensure_user(spec)
	_seed_pos_and_lojas(company, warehouses, cost_centers)
	for spec in DEMO_USERS:
		_ensure_user(spec, assign_links=True)
	_ensure_employees(company)
	_grant_sector_warehouses(warehouses)
	frappe.clear_cache()


def _company() -> str | None:
	import frappe

	if frappe.db.exists("Company", COMPANY_NAME):
		return COMPANY_NAME
	return frappe.db.get_value("Company", {}, "name")


def _abbr(company: str) -> str:
	import frappe

	return frappe.db.get_value("Company", company, "abbr")


def _ensure_roles() -> None:
	import frappe

	for role_name in (ROLE_DONO, ROLE_GERENTE, ROLE_CAIXA, ROLE_ESTOQUISTA, ROLE_FABRICACAO):
		if frappe.db.exists("Role", role_name):
			frappe.db.set_value("Role", role_name, "desk_access", 1, update_modified=False)
			continue
		role = frappe.new_doc("Role")
		role.role_name = role_name
		role.desk_access = 1
		role.insert(ignore_permissions=True)


def _ensure_role_profiles() -> None:
	import frappe

	for role_name in (ROLE_DONO, ROLE_GERENTE, ROLE_CAIXA, ROLE_ESTOQUISTA, ROLE_FABRICACAO):
		current = frappe.get_all(
			"Has Role",
			filters={"parent": role_name, "parenttype": "Role Profile"},
			pluck="role",
		)
		if current == [role_name]:
			continue
		if frappe.db.exists("Role Profile", role_name):
			profile = frappe.get_doc("Role Profile", role_name)
			if profile.is_locked:
				profile.unlock()
		else:
			profile = frappe.new_doc("Role Profile")
			profile.role_profile = role_name
		profile.set("roles", [{"role": role_name}])
		profile.save(ignore_permissions=True)


def _ensure_custom_fields() -> None:
	_custom_field(
		"Item",
		"catalogo",
		{
			"label": "Catálogo",
			"fieldtype": "Select",
			"options": "Produto\nVela",
			"insert_after": "item_group",
			"in_list_view": 1,
			"in_standard_filter": 1,
			"description": "Produto é o catálogo da loja. Vela é o espaço da fabricação, ainda sem receita.",
		},
	)
	_custom_field(
		"Employee",
		"loja",
		{
			"label": "Loja",
			"fieldtype": "Link",
			"options": "Loja",
			"insert_after": "company",
			"in_list_view": 1,
			"in_standard_filter": 1,
		},
	)
	_custom_field(
		"User",
		"loja",
		{
			"label": "Loja",
			"fieldtype": "Link",
			"options": "Loja",
			"insert_after": "role_profile_name",
			"in_list_view": 1,
			"in_standard_filter": 1,
			"description": "Em branco, a pessoa vê todas as lojas. O dono fica em branco.",
		},
	)


def _custom_field(doctype: str, fieldname: str, props: dict) -> None:
	import frappe

	name = f"{doctype}-{fieldname}"
	if frappe.db.exists("Custom Field", name):
		return
	field = frappe.new_doc("Custom Field")
	field.dt = doctype
	field.fieldname = fieldname
	field.module = MODULE
	for key, value in props.items():
		setattr(field, key, value)
	field.insert(ignore_permissions=True)


def _ensure_docperms() -> None:
	import frappe
	from frappe.permissions import setup_custom_perms

	flags = (
		"select",
		"read",
		"write",
		"create",
		"delete",
		"submit",
		"cancel",
		"amend",
		"report",
		"export",
		"import",
		"share",
		"print",
		"email",
	)
	for doctype, roles in ROLE_PERMS.items():
		if not frappe.db.exists("DocType", doctype):
			continue
		setup_custom_perms(doctype)
		for role, granted in roles.items():
			values = {flag: 1 if granted.get(flag) else 0 for flag in flags}
			values.update({"permlevel": 0, "if_owner": 0})
			existing = frappe.db.get_value(
				"Custom DocPerm",
				{"parent": doctype, "role": role, "permlevel": 0, "if_owner": 0},
				"name",
			)
			if existing:
				frappe.db.set_value("Custom DocPerm", existing, values, update_modified=False)
				continue
			perm = frappe.new_doc("Custom DocPerm")
			perm.parent = doctype
			perm.parenttype = "DocType"
			perm.parentfield = "permissions"
			perm.role = role
			for key, value in values.items():
				setattr(perm, key, value)
			perm.insert(ignore_permissions=True)


def _seed_warehouses(company: str) -> dict:
	import frappe

	abbr = _abbr(company)
	root = _root_name("Warehouse", company, "parent_warehouse")
	if not root:
		root = _ensure_warehouse(company, "Todos os depósitos", None, is_group=1)

	central = _ensure_warehouse(company, "Central", root, is_group=0)
	stores_name = f"Lojas - {abbr}"
	current_default = frappe.db.get_value("Company", company, "default_warehouse")
	default_is_group = current_default and frappe.db.get_value("Warehouse", current_default, "is_group")
	if current_default in (None, "", stores_name) or default_is_group:
		frappe.db.set_value("Company", company, "default_warehouse", central, update_modified=False)

	if frappe.db.exists("Warehouse", stores_name):
		stores_group = stores_name
		group = frappe.get_doc("Warehouse", stores_name)
		if not group.is_group:
			group.is_group = 1
			group.save(ignore_permissions=True)
	else:
		stores_group = _ensure_warehouse(company, "Lojas", root, is_group=1)

	store_warehouses = [
		_ensure_warehouse(company, f"Loja {index}", stores_group, is_group=0) for index in range(1, 6)
	]
	fabrication = _ensure_warehouse(company, "Fabricação", root, is_group=1)
	insumos = _ensure_warehouse(company, "Fabricação - Insumos", fabrication, is_group=0)
	acabadas = _ensure_warehouse(company, "Fabricação - Velas acabadas", fabrication, is_group=0)
	for legacy in (f"Trabalho Em Andamento - {abbr}", f"Produtos Acabados - {abbr}"):
		if not frappe.db.exists("Warehouse", legacy):
			continue
		doc = frappe.get_doc("Warehouse", legacy)
		if doc.parent_warehouse != fabrication:
			doc.parent_warehouse = fabrication
			doc.save(ignore_permissions=True)

	transit = _ensure_transit(company, root, abbr)
	if transit:
		frappe.db.set_value("Company", company, "default_in_transit_warehouse", transit, update_modified=False)

	frappe.utils.nestedset.rebuild_tree("Warehouse")
	return {
		"central": central,
		"stores": store_warehouses,
		"insumos": insumos,
		"acabadas": acabadas,
		"transit": transit,
	}


def _ensure_transit(company: str, root: str, abbr: str) -> str:
	import frappe

	for name in (
		f"Mercadorias Em Trânsito - {abbr}",
		f"Em trânsito - {abbr}",
		f"Goods In Transit - {abbr}",
	):
		if not frappe.db.exists("Warehouse", name):
			continue
		doc = frappe.get_doc("Warehouse", name)
		if doc.parent_warehouse != root:
			doc.parent_warehouse = root
			doc.save(ignore_permissions=True)
		return doc.name
	if frappe.db.exists("Warehouse Type", "Transit"):
		return _ensure_warehouse(company, "Em trânsito", root, is_group=0, warehouse_type="Transit")
	return _ensure_warehouse(company, "Em trânsito", root, is_group=0)


def _ensure_warehouse(company: str, warehouse_name: str, parent: str | None, is_group: int, warehouse_type: str | None = None) -> str:
	import frappe

	name = f"{warehouse_name} - {_abbr(company)}"
	if frappe.db.exists("Warehouse", name):
		doc = frappe.get_doc("Warehouse", name)
		changed = False
		if parent and doc.parent_warehouse != parent:
			doc.parent_warehouse = parent
			changed = True
		if int(doc.is_group or 0) != int(is_group):
			doc.is_group = is_group
			changed = True
		if warehouse_type and doc.warehouse_type != warehouse_type:
			doc.warehouse_type = warehouse_type
			changed = True
		if changed:
			doc.save(ignore_permissions=True)
		return doc.name

	doc = frappe.new_doc("Warehouse")
	doc.warehouse_name = warehouse_name
	doc.company = company
	doc.is_group = is_group
	if parent:
		doc.parent_warehouse = parent
	if warehouse_type:
		doc.warehouse_type = warehouse_type
	doc.flags.ignore_inventory_account_validation = True
	doc.insert(ignore_permissions=True)
	return doc.name


def _seed_cost_centers(company: str) -> dict:
	root = _root_name("Cost Center", company, "parent_cost_center")
	if not root:
		raise RuntimeError(f"A empresa {company} não tem centro de custo raiz.")
	named = {index: _ensure_cost_center(company, f"Loja {index}", root) for index in range(1, 6)}
	named["central"] = _ensure_cost_center(company, "Central", root)
	named["fabricacao"] = _ensure_cost_center(company, "Fabricação", root)
	return named


def _ensure_cost_center(company: str, cost_center_name: str, parent: str) -> str:
	import frappe

	name = f"{cost_center_name} - {_abbr(company)}"
	if frappe.db.exists("Cost Center", name):
		return name
	doc = frappe.new_doc("Cost Center")
	doc.cost_center_name = cost_center_name
	doc.company = company
	doc.parent_cost_center = parent
	doc.is_group = 0
	doc.insert(ignore_permissions=True)
	return doc.name


def _root_name(doctype: str, company: str, parent_field: str) -> str | None:
	import frappe

	rows = frappe.get_all(doctype, filters={"company": company, "is_group": 1}, fields=["name", parent_field])
	for row in rows:
		if not row.get(parent_field):
			return row.name
	return None


def _seed_catalog(company: str) -> None:
	import frappe

	parent = _item_group_root()
	for group_name in ("Velas", "Presentes", "Casa e decoração", "Insumos de vela"):
		_ensure_item_group(group_name, parent)

	if not frappe.db.exists("UOM", "Unidade"):
		uom = frappe.new_doc("UOM")
		uom.uom_name = "Unidade"
		uom.must_be_whole_number = 1
		uom.insert(ignore_permissions=True)

	if not frappe.db.exists("Price List", PRICE_LIST_NAME):
		price_list = frappe.new_doc("Price List")
		price_list.price_list_name = PRICE_LIST_NAME
		price_list.currency = "BRL"
		price_list.selling = 1
		price_list.buying = 0
		price_list.enabled = 1
		price_list.insert(ignore_permissions=True)

	for code, item_name, group, rate, catalogo in PRODUCTS:
		if frappe.db.exists("Item", code):
			frappe.db.set_value("Item", code, {"item_name": item_name, "catalogo": catalogo}, update_modified=False)
		else:
			item = frappe.new_doc("Item")
			item.item_code = code
			item.item_name = item_name
			item.item_group = group
			item.stock_uom = "Unidade"
			item.is_stock_item = 1
			item.include_item_in_manufacturing = 0
			item.catalogo = catalogo
			item.description = item_name
			item.insert(ignore_permissions=True)
		_ensure_item_price(code, rate)


def _item_group_root() -> str:
	import frappe

	if frappe.db.exists("Item Group", "All Item Groups"):
		return "All Item Groups"
	rows = frappe.get_all("Item Group", filters={"is_group": 1}, fields=["name", "parent_item_group"])
	for row in rows:
		if not row.parent_item_group:
			return row.name
	return rows[0].name


def _ensure_item_group(name: str, parent: str) -> None:
	import frappe

	if frappe.db.exists("Item Group", name):
		return
	group = frappe.new_doc("Item Group")
	group.item_group_name = name
	group.parent_item_group = parent
	group.is_group = 0
	group.insert(ignore_permissions=True)


def _ensure_item_price(item_code: str, rate: float) -> None:
	import frappe

	existing = frappe.db.get_value(
		"Item Price",
		{"item_code": item_code, "price_list": PRICE_LIST_NAME, "uom": "Unidade"},
		"name",
	)
	if existing:
		frappe.db.set_value("Item Price", existing, "price_list_rate", rate, update_modified=False)
		return
	price = frappe.new_doc("Item Price")
	price.item_code = item_code
	price.uom = "Unidade"
	price.price_list = PRICE_LIST_NAME
	price.price_list_rate = rate
	price.selling = 1
	price.insert(ignore_permissions=True)


def _ensure_customer(company: str) -> None:
	import frappe

	if frappe.db.exists("Customer", {"customer_name": CUSTOMER_NAME}):
		return
	customer = frappe.new_doc("Customer")
	customer.customer_name = CUSTOMER_NAME
	customer.naming_series = "CUST-.YYYY.-"
	customer.customer_type = "Individual"
	customer.customer_group = _first_existing("Customer Group", ("Individual", "All Customer Groups"))
	customer.territory = _first_existing("Territory", ("Brazil", "All Territories"))
	customer.insert(ignore_permissions=True)


def _first_existing(doctype: str, names: tuple[str, ...]) -> str:
	import frappe

	for name in names:
		if frappe.db.exists(doctype, name):
			return name
	found = frappe.db.get_value(doctype, {}, "name")
	if not found:
		raise RuntimeError(f"Não há registro de {doctype} para a carga da V1.")
	return found


def _seed_pos_and_lojas(company: str, warehouses: dict, cost_centers: dict) -> None:
	import frappe

	account = frappe.db.get_value("Company", company, "write_off_account") or f"Abatimento - {_abbr(company)}"
	customer = frappe.db.get_value("Customer", {"customer_name": CUSTOMER_NAME}, "name")
	for index, loja_name in enumerate(LOJA_NAMES, start=1):
		users = _pos_users(index)
		profile = _ensure_pos_profile(
			company,
			index,
			warehouses["stores"][index - 1],
			cost_centers[index],
			account,
			customer,
			users,
		)
		address = _ensure_address(loja_name, index)
		gerente = next(
			(spec["email"] for spec in DEMO_USERS if spec["profile"] == ROLE_GERENTE and spec["loja_index"] == index),
			None,
		)
		_ensure_loja(
			loja_name,
			company,
			warehouses["stores"][index - 1],
			cost_centers[index],
			profile,
			gerente,
			address,
			index,
		)


def _pos_users(index: int) -> list[dict]:
	rows = []
	for spec in DEMO_USERS:
		if spec["loja_index"] != index:
			continue
		if spec["profile"] not in {ROLE_GERENTE, ROLE_CAIXA}:
			continue
		rows.append({"user": spec["email"], "default": 1})
	return rows


def _ensure_pos_profile(company, index, warehouse, cost_center, account, customer, users) -> str:
	import frappe

	name = f"PDV Loja {index}"
	if frappe.db.exists("POS Profile", name):
		doc = frappe.get_doc("POS Profile", name)
	else:
		doc = frappe.new_doc("POS Profile")
		doc.__newname = name
	doc.company = company
	doc.currency = "BRL"
	doc.warehouse = warehouse
	doc.cost_center = cost_center
	doc.write_off_account = account
	doc.write_off_cost_center = cost_center
	doc.write_off_limit = 1
	doc.customer = customer
	doc.selling_price_list = PRICE_LIST_NAME
	doc.disabled = 0
	doc.set("payments", [{"mode_of_payment": "Cash", "default": 1}])
	doc.set("applicable_for_users", users)
	doc.save(ignore_permissions=True)
	return doc.name


def _ensure_address(loja_name: str, index: int) -> str:
	import frappe

	title = loja_name
	existing = frappe.db.get_value("Address", {"address_title": title}, "name")
	if existing:
		return existing
	address = frappe.new_doc("Address")
	address.address_title = title
	address.address_type = "Shop"
	address.address_line1 = f"Rua das Flores, {100 + index}"
	address.city = "São Paulo"
	address.state = "SP"
	address.pincode = f"0100{index}-000"
	address.country = "Brazil"
	address.insert(ignore_permissions=True)
	return address.name


def _ensure_loja(name, company, warehouse, cost_center, profile, gerente, address, index) -> None:
	import frappe

	if frappe.db.exists("Loja", name):
		doc = frappe.get_doc("Loja", name)
	else:
		doc = frappe.new_doc("Loja")
		doc.nome = name
	doc.empresa = company
	doc.deposito = warehouse
	doc.centro_de_custo = cost_center
	doc.perfil_de_pdv = profile
	doc.gerente = gerente
	doc.endereco = address
	doc.ativa = 1
	doc.endereco_fiscal = (
		f"Rua das Flores, {100 + index} — São Paulo/SP. "
		"CNPJ e inscrição estadual ficam em aberto até a definição fiscal."
	)
	doc.save(ignore_permissions=True)


def _ensure_user(spec: dict, assign_links: bool = False) -> None:
	import frappe

	email = spec["email"]
	if frappe.db.exists("User", email):
		user = frappe.get_doc("User", email)
	else:
		user = frappe.new_doc("User")
		user.email = email
		user.first_name = spec["first_name"]
		user.send_welcome_email = 0
		user.new_password = DEMO_PASSWORD
	user.enabled = 1
	user.user_type = "System User"
	user.language = "pt-BR"
	user.time_zone = "America/Sao_Paulo"
	user.send_welcome_email = 0
	user.set("role_profiles", [{"role_profile": spec["profile"]}])
	if assign_links:
		loja_name = LOJA_NAMES[spec["loja_index"] - 1] if spec["loja_index"] else None
		if loja_name and frappe.db.exists("Loja", loja_name):
			user.loja = loja_name
		elif not spec["loja_index"]:
			user.loja = None
		if spec["workspace"] and frappe.db.exists("Workspace", spec["workspace"]):
			user.default_workspace = spec["workspace"]
	user.save(ignore_permissions=True)


def _ensure_employees(company: str) -> None:
	import frappe

	for offset, spec in enumerate(DEMO_USERS, start=1):
		if spec["profile"] not in {ROLE_GERENTE, ROLE_CAIXA}:
			continue
		if frappe.db.exists("Employee", {"user_id": spec["email"]}):
			name = frappe.db.get_value("Employee", {"user_id": spec["email"]}, "name")
			loja_name = LOJA_NAMES[spec["loja_index"] - 1]
			frappe.db.set_value("Employee", name, {"loja": loja_name, "create_user_permission": 0}, update_modified=False)
			continue
		employee = frappe.new_doc("Employee")
		employee.first_name = spec["first_name"]
		employee.company = company
		employee.gender = spec["gender"]
		employee.date_of_birth = f"1990-0{min(offset, 9)}-15"
		employee.date_of_joining = "2024-02-01"
		employee.status = "Active"
		employee.user_id = spec["email"]
		employee.loja = LOJA_NAMES[spec["loja_index"] - 1]
		employee.create_user_permission = 0
		employee.insert(ignore_permissions=True)


def _grant_sector_warehouses(warehouses: dict) -> None:
	from frappe.permissions import add_user_permission

	add_user_permission(
		"Warehouse",
		warehouses["central"],
		"estoquista@flor.localhost",
		ignore_permissions=True,
		applicable_for="Warehouse",
	)
	for key in ("insumos", "acabadas"):
		add_user_permission(
			"Warehouse",
			warehouses[key],
			"fabricacao@flor.localhost",
			ignore_permissions=True,
			applicable_for="Warehouse",
		)


def _ensure_workspaces() -> None:
	_ensure_number_card("Lojas da Flor de Lótus", "Loja")
	_ensure_number_card("Produtos da Flor de Lótus", "Item")
	_ensure_number_card("Funcionários da Flor de Lótus", "Employee")
	_ensure_number_card("Depósitos da Flor de Lótus", "Warehouse")

	_ensure_workspace(
		WS_DONO,
		ROLE_DONO,
		"store",
		0.1,
		"Visão geral",
		"As cinco lojas, o estoque central e os cadastros. O lucro consolidado entra numa versão seguinte.",
		[
			("Lojas da Flor de Lótus", 3),
			("Produtos da Flor de Lótus", 3),
			("Funcionários da Flor de Lótus", 3),
			("Depósitos da Flor de Lótus", 3),
		],
		[
			("Lojas", "Loja", "List", "store"),
			("Produtos", "Item", "List", "package"),
			("Usuários", "User", "List", "users"),
			("Estoque central", "Warehouse", "Tree", "warehouse"),
			("Funcionários", "Employee", "List", "users"),
		],
		[
			(
				"Cadastros",
				[
					("Lojas", "Loja"),
					("Produtos", "Item"),
					("Preços", "Item Price"),
					("Usuários", "User"),
					("Funcionários", "Employee"),
				],
			),
			(
				"Estoque",
				[
					("Depósitos", "Warehouse"),
					("Centros de custo", "Cost Center"),
				],
			),
		],
	)
	_ensure_workspace(
		WS_GERENTE,
		ROLE_GERENTE,
		"store",
		0.2,
		"Minha loja",
		"Caixa, estoque, funcionários e produtos desta loja. Outra loja e o lucro consolidado não aparecem aqui.",
		[
			("Lojas da Flor de Lótus", 4),
			("Produtos da Flor de Lótus", 4),
			("Funcionários da Flor de Lótus", 4),
		],
		[
			("Abertura de caixa", "POS Opening Entry", "List", "store"),
			("Fechamento de caixa", "POS Closing Entry", "List", "store"),
			("Estoque da loja", "Warehouse", "List", "warehouse"),
			("Funcionários", "Employee", "List", "users"),
			("Produtos", "Item", "List", "package"),
		],
		[
			(
				"Loja",
				[
					("Abertura de caixa", "POS Opening Entry"),
					("Fechamento de caixa", "POS Closing Entry"),
					("Vendas", "POS Invoice"),
					("Funcionários", "Employee"),
					("Produtos", "Item"),
				],
			)
		],
	)
	_ensure_workspace(
		WS_CAIXA,
		ROLE_CAIXA,
		"store",
		0.3,
		"Caixa",
		"Abra o caixa, acompanhe as vendas da sua loja e feche o caixa. Cadastro de produto, preço e usuário não é desta função.",
		[("Produtos da Flor de Lótus", 4)],
		[
			("Abrir caixa", "POS Opening Entry", "New", "store"),
			("Fechar caixa", "POS Closing Entry", "New", "store"),
			("Vendas", "POS Invoice", "List", "package"),
			("PDV", "point-of-sale", "Page", "store"),
		],
		[
			(
				"Caixa",
				[
					("Abertura de caixa", "POS Opening Entry"),
					("Fechamento de caixa", "POS Closing Entry"),
					("Vendas", "POS Invoice"),
				],
			)
		],
	)


def _ensure_number_card(label: str, document_type: str) -> None:
	import frappe

	if frappe.db.exists("Number Card", label):
		return
	card = frappe.new_doc("Number Card")
	card.label = label
	card.type = "Document Type"
	card.document_type = document_type
	card.function = "Count"
	card.is_public = 1
	card.module = MODULE
	card.show_percentage_stats = 0
	card.filters_json = "[]"
	card.insert(ignore_permissions=True)


def _ensure_workspace(label, role, icon, sequence, header, paragraph, cards, shortcuts, link_groups) -> None:
	import frappe
	from frappe.desk.doctype.workspace.workspace import sanitize_content

	if frappe.db.exists("Workspace", label):
		workspace = frappe.get_doc("Workspace", label)
	else:
		workspace = frappe.new_doc("Workspace")
		workspace.label = label
	workspace.title = label
	workspace.icon = icon
	workspace.module = MODULE
	workspace.public = 1
	workspace.is_hidden = 0
	workspace.sequence_id = sequence
	workspace.type = "Workspace"
	workspace.set("roles", [{"role": role}])
	workspace.set(
		"number_cards",
		[{"number_card_name": name, "label": name} for name, _col in cards],
	)

	shortcut_rows = []
	content = [
		{"id": "fdl-header", "type": "header", "data": {"text": header, "col": 12}},
		{"id": "fdl-paragraph", "type": "paragraph", "data": {"text": paragraph, "col": 12}},
	]
	for name, col in cards:
		content.append(
			{"id": f"fdl-card-{_slug(name)}", "type": "number_card", "data": {"number_card_name": name, "col": col}}
		)
	for shortcut_label, link_to, view, shortcut_icon in shortcuts:
		if view == "Page":
			shortcut_rows.append({"type": "Page", "link_to": link_to, "label": shortcut_label, "icon": shortcut_icon})
		else:
			shortcut_rows.append(
				{
					"type": "DocType",
					"link_to": link_to,
					"label": shortcut_label,
					"doc_view": view,
					"icon": shortcut_icon,
					"color": PALETTE["primary"],
				}
			)
		content.append(
			{
				"id": f"fdl-shortcut-{_slug(shortcut_label)}",
				"type": "shortcut",
				"data": {"shortcut_name": shortcut_label, "col": 3},
			}
		)
	workspace.set("shortcuts", shortcut_rows)

	links = []
	for card_label, items in link_groups:
		links.append({"type": "Card Break", "label": card_label, "link_count": len(items)})
		content.append(
			{"id": f"fdl-links-{_slug(card_label)}", "type": "card", "data": {"card_name": card_label, "col": 4}}
		)
		for item_label, link_to in items:
			links.append({"type": "Link", "label": item_label, "link_type": "DocType", "link_to": link_to})
	workspace.set("links", links)
	workspace.content = sanitize_content(json.dumps(content))
	workspace.flags.ignore_links = True
	workspace.save(ignore_permissions=True)


def _slug(value: str) -> str:
	cleaned = []
	for char in value.lower():
		if char.isalnum():
			cleaned.append(char)
		else:
			cleaned.append("-")
	return "".join(cleaned).strip("-")
