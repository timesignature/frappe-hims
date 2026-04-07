# Copyright (c) 2026, Shelton Tembo and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ClinicalNote(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		date_created: DF.Datetime | None
		episode_no: DF.Link
		notes: DF.SmallText | None
		patient_name: DF.Data | None
		patient_no: DF.Data | None
	# end: auto-generated types

	pass
