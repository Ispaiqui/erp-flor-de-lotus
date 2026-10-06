# Copyright (c) 2026, Flor de Lótus and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Loja(Document):
	def validate(self):
		if self.deposito and frappe.db.get_value("Warehouse", self.deposito, "is_group"):
			frappe.throw(_("O depósito da loja precisa ser um depósito de verdade, não um grupo."))

		if self.deposito and self.empresa:
			company = frappe.db.get_value("Warehouse", self.deposito, "company")
			if company and company != self.empresa:
				frappe.throw(_("O depósito precisa ser da mesma empresa da loja."))

		if self.centro_de_custo and self.empresa:
			company = frappe.db.get_value("Cost Center", self.centro_de_custo, "company")
			if company and company != self.empresa:
				frappe.throw(_("O centro de custo precisa ser da mesma empresa da loja."))
