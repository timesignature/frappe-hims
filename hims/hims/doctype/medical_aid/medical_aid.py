# Copyright (c) 2026, Shelton Tembo and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from hims.utils import ref


class MedicalAid(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        customer: DF.Link | None
        email: DF.Data
        funder_code: DF.Data
        phone: DF.Data
        title: DF.Data
    # end: auto-generated types

    def after_insert(self):
        doc = ref("Customer")
        doc.customer_name = self.name
        doc.customer_type = "Commercial"
        doc.customer_group = "Commercial"
        doc.save()

        med = ref("Medical Aid").find(self.name)
        med.customer = doc.name
        med.save()
