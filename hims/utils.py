import frappe


class Ref:
    def __init__(self, doctype, name=None):
        # Use object.__setattr__ to bypass the custom __setattr__ logic during init
        object.__setattr__(self, "doctype", doctype)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "data", {})
        object.__setattr__(self, "_filters", {})

    def __setattr__(self, name, value):
        """Allows setting fields directly: ref.status = 'Open' maps to ref.data['status']"""
        internals = ["doctype", "name", "data", "_filters"]
        if name in internals:
            object.__setattr__(self, name, value)
        else:
            self.data[name] = value

    def __getattr__(self, name):
        """Allows getting fields directly: print(ref.status) reads from ref.data['status']"""
        if name in self.data:
            return self.data[name]
        raise AttributeError(f"'{self.doctype}' object has no attribute '{name}'")

    def find(self, name):
        """Fetches a single document and returns a populated Ref instance."""
        doc = frappe.get_doc(self.doctype, name)
        new_ref = Ref(self.doctype, name=name)
        new_ref.data = doc.as_dict()
        return new_ref

    def where(self, filters):
        """Stores filters for a list query. Returns self for chaining."""
        if isinstance(filters, dict):
            self._filters.update(filters)
        return self

    def get(self, fields=["*"], limit=0):
        """Executes a list query using stored filters."""
        return frappe.get_all(
            self.doctype, filters=self._filters, fields=fields, limit_page_length=limit
        )

    def all(self):
        """Returns all records for the doctype."""
        return frappe.get_all(self.doctype, fields=["*"])

    def save(self):
        """Updates the record if 'name' exists, otherwise inserts a new one."""
        if self.name:
            # Update existing
            doc = frappe.get_doc(self.doctype, self.name)
            doc.update(self.data)
            doc.save()
        else:
            # Create new
            doc = frappe.get_doc({"doctype": self.doctype, **self.data})
            doc.insert()
            # Update the instance name with the new ID
            object.__setattr__(self, "name", doc.name)

        return self

    def delete(self, name=None):
        """Deletes the document by name or current instance name."""
        target = name or self.name
        if not target:
            frappe.throw("Please provide a name or find a record to delete.")

        frappe.delete_doc(self.doctype, target)

        if target == self.name:
            object.__setattr__(self, "name", None)

        return self


def ref(doctype):
    return Ref(doctype)
