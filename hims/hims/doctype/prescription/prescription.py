# Copyright (c) 2026, Shelton Tembo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Prescription(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF
        from hims.hims.doctype.prescription_lines.prescription_lines import (
            PrescriptionLines,
        )

        amended_from: DF.Link | None
        date_created: DF.Datetime
        episode_no: DF.Link
        items: DF.Table[PrescriptionLines]
        notes: DF.SmallText | None
        patient_name: DF.Data | None
        patient_no: DF.Data | None
        status: DF.Literal["", "Open", "Dispensed", "Cancelled"]
    # end: auto-generated types

    def before_insert(self):
        self.date_created = frappe.utils.now_datetime()
