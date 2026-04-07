# Copyright (c) 2026, Shelton Tembo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from hims.utils import ref


class Ward(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        capacity: DF.Data | None
        description: DF.Data | None

    # end: auto-generated types
    @property
    def capacity(self):
        try:
            doc = ref("Bed").where({"ward": self.name}).get()
            return len(doc)
        except Exception as e:
            frappe.log_error(message=str(e), title="Ward Capacity Error")
            return 0
