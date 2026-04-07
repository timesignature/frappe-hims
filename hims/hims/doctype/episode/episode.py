# Copyright (c) 2026, Shelton Tembo and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from hims.utils import ref


class Episode(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        admission_date: DF.Datetime
        admission_type: DF.Literal["", "OPD", "IPD"]
        bed: DF.Data | None
        discharge_comment: DF.SmallText | None
        discharge_date: DF.Datetime | None
        discharge_status: DF.Literal["", "Stable", "Death", "Referred"]
        dob: DF.Date | None
        gender: DF.Data | None
        patient_name: DF.Data | None
        patient_no: DF.Link
        status: DF.Literal["", "Open", "Closed", "Cancelled"]
        ward: DF.Data | None
    # end: auto-generated types

    @property
    def balance(self):
        try:
            doc = ref("Sales Invoice").where({"episode_no": self.name}).get()
            total = 0

            for x in doc:
                total += x.outstanding_amount
            return total

        except Exception:
            return 0

    @property
    def funder(self):
        try:
            doc = ref("Patient").find(self.patient_no)
            return (
                "Funded By Medical Aid" if doc.has_medical_aid else "Funded By Patient"
            )
        except Exception:
            return "Patient Not Found"
