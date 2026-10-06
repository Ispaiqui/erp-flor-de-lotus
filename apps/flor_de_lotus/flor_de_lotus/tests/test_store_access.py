# Copyright (c) 2026, Flor de Lótus and Contributors
# License: GNU General Public License v3. See license.txt

"""Usuário de uma loja não lê nem grava documento de outra pela API."""

from __future__ import annotations

import frappe
from frappe.tests import IntegrationTestCase

from flor_de_lotus.setup_v1 import COMPANY_NAME, LOJA_NAMES

GERENTE_1 = "gerente.loja1@flor.localhost"
CAIXA_1 = "caixa.loja1@flor.localhost"
DONO = "dono@flor.localhost"
FABRICACAO = "fabricacao@flor.localhost"
LOJA_1 = LOJA_NAMES[0]
LOJA_2 = LOJA_NAMES[1]


class TestStoreAccess(IntegrationTestCase):
	def tearDown(self):
		frappe.set_user("Administrator")
		super().tearDown()

	def test_demo_records_exist(self):
		self.assertTrue(frappe.db.exists("Loja", LOJA_1))
		self.assertTrue(frappe.db.exists("Loja", LOJA_2))
		self.assertTrue(frappe.db.exists("User", GERENTE_1))
		self.assertTrue(frappe.db.exists("Item", "FDL-001"))
		self.assertTrue(frappe.db.exists("Item", "FDL-016"))

	def test_gerente_cannot_read_or_write_another_store(self):
		other_employee = frappe.db.get_value("Employee", {"user_id": "caixa.loja2@flor.localhost"}, "name")
		other_warehouse = frappe.db.get_value("Loja", LOJA_2, "deposito")
		self.assertTrue(other_employee)
		self.assertTrue(other_warehouse)

		frappe.set_user(GERENTE_1)
		self.assertFalse(frappe.has_permission("Loja", "read", LOJA_2))
		self.assertFalse(frappe.has_permission("Loja", "write", LOJA_2))
		self.assertFalse(frappe.has_permission("Loja", "write", LOJA_1))
		with self.assertRaises(frappe.PermissionError):
			frappe.get_doc("Loja", LOJA_2)
		with self.assertRaises(frappe.PermissionError):
			frappe.get_doc("Employee", other_employee)

		names = frappe.get_list("Loja", pluck="name", limit_page_length=20)
		self.assertIn(LOJA_1, names)
		self.assertNotIn(LOJA_2, names)

		warehouses = frappe.get_list("Warehouse", pluck="name", limit_page_length=50)
		self.assertNotIn(other_warehouse, warehouses)

		item = frappe.get_doc("Item", "FDL-001")
		item.item_name = "Alteração proibida"
		with self.assertRaises(frappe.PermissionError):
			item.save()

		with self.assertRaises((frappe.PermissionError, frappe.ValidationError)):
			frappe.get_doc(
				{
					"doctype": "Employee",
					"first_name": "Fora da loja",
					"company": COMPANY_NAME,
					"status": "Active",
					"gender": "Female",
					"date_of_birth": "1991-04-02",
					"date_of_joining": "2024-03-01",
					"loja": LOJA_2,
				}
			).insert()

		company = frappe.get_doc("Company", COMPANY_NAME)
		self.assertEqual(company.name, COMPANY_NAME)

	def test_caixa_cannot_read_or_write_another_store(self):
		other_warehouse = frappe.db.get_value("Loja", LOJA_2, "deposito")
		other_profile = frappe.db.get_value("Loja", LOJA_2, "perfil_de_pdv")

		frappe.set_user(CAIXA_1)
		self.assertFalse(frappe.has_permission("Loja", "read", LOJA_2))
		self.assertFalse(frappe.has_permission("Loja", "write", LOJA_2))
		self.assertFalse(frappe.has_permission("Employee", "read"))
		self.assertFalse(frappe.has_permission("Item", "write", "FDL-001"))
		with self.assertRaises(frappe.PermissionError):
			frappe.get_doc("Loja", LOJA_2)

		names = frappe.get_list("Loja", pluck="name", limit_page_length=20)
		self.assertIn(LOJA_1, names)
		self.assertNotIn(LOJA_2, names)
		warehouses = frappe.get_list("Warehouse", pluck="name", limit_page_length=50)
		self.assertNotIn(other_warehouse, warehouses)
		profiles = frappe.get_list("POS Profile", pluck="name", limit_page_length=20)
		self.assertNotIn(other_profile, profiles)
		self.assertTrue(profiles)

	def test_dono_reads_every_store(self):
		frappe.set_user(DONO)
		frappe.get_doc("Loja", LOJA_1)
		frappe.get_doc("Loja", LOJA_2)
		names = frappe.get_list("Loja", pluck="name", limit_page_length=20)
		self.assertIn(LOJA_1, names)
		self.assertIn(LOJA_2, names)

	def test_fabricacao_reads_only_vela_items(self):
		frappe.set_user(FABRICACAO)
		codes = frappe.get_list("Item", pluck="name", limit_page_length=50)
		self.assertIn("FDL-016", codes)
		self.assertNotIn("FDL-001", codes)
		with self.assertRaises(frappe.PermissionError):
			frappe.get_doc("Item", "FDL-001")
		frappe.get_doc("Item", "FDL-016")
