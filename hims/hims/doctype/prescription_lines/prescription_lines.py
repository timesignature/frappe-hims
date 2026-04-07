# Copyright (c) 2026, Shelton Tembo and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class PrescriptionLines(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		dosage: DF.Data | None
		drug_description: DF.Data | None
		duration: DF.Data | None
		frequency: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		route: DF.Data | None
	# end: auto-generated types

	pass
