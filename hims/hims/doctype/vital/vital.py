# Copyright (c) 2026, Shelton Tembo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Vital(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        amended_from: DF.Link | None
        blood_pressure: DF.Data | None
        body_temperature: DF.Data | None
        date_created: DF.Datetime | None
        episode_no: DF.Link
        height: DF.Data | None
        level_of_consciousness: DF.Data | None
        oxygen_saturation: DF.Data | None
        pain_level: DF.Data | None
        patient_name: DF.Data | None
        patient_no: DF.Data
        pulse: DF.Data | None
        respiratory_rate: DF.Data | None
        weight: DF.Data | None
    # end: auto-generated types

    def before_insert(self):
        self.date_created = frappe.utils.now_datetime()
