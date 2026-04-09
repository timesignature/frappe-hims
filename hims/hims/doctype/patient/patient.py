# Copyright (c) 2026, Shelton Tembo and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from hims.utils import ref


class Patient(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        address: DF.SmallText | None
        clergy: DF.Link | None
        customer: DF.Link | None
        dob: DF.Date
        email: DF.Data | None
        first_name: DF.Data
        full_name: DF.Data | None
        funder: DF.Link | None
        funder_code: DF.Data | None
        funder_name: DF.Data | None
        funder_phone: DF.Data | None
        gender: DF.Literal["", "Male", "Female"]
        has_medical_aid: DF.Check
        have_whatsapp: DF.Check
        last_name: DF.Data
        national_id: DF.Data
        phone: DF.Data | None
        religion: DF.Link | None
    # end: auto-generated types

    def before_insert(self):
        self.full_name = f"{self.first_name} {self.last_name}"

    def after_insert(self):
        doc = ref("Customer")
        doc.customer_name = self.name
        doc.customer_type = "Individual"
        doc.customer_group = "Individual"
        doc.gender = self.gender
        doc.save()

        patient = ref("Patient").find(self.name)
        patient.customer = doc.name
        patient.save()

    @property
    def balance(self):
        try:
            doc = ref("Sales Invoice").where({"customer": self.name}).get()
            total = 0
            for x in doc:
                total += x.outstanding_amount

            return total
        except Exception:
            return 0
