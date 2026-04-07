class Ref {
    constructor(doctype, name = null) {
        this.doctype = doctype;
        this.name = name;
        this.data = {};
        this._filters = null;

        return new Proxy(this, {
            set: (target, prop, value) => {
                const internals = ['doctype', 'name', 'data', '_filters'];
                if (internals.includes(prop)) {
                    target[prop] = value;
                } else {
                    target.data[prop] = value;
                }
                return true;
            },
            get: (target, prop) => {
                // IMPORTANT: Check if the property exists on the class first (methods/internals)
                if (prop in target) {
                    let value = target[prop];
                    // If it's a function, bind it to the target so 'this' works correctly
                    if (typeof value === 'function') {
                        return value.bind(target);
                    }
                    return value;
                }
                // Otherwise, look in the data object (fields)
                return target.data[prop];
            }
        });
    }

    async find(name) {
        const doc = await frappe.db.get_doc(this.doctype, name);
        let instance = new Ref(this.doctype, name);
        instance.data = doc;
        return instance;
    }

    async all() {
        return await frappe.db.get_list(this.doctype, { fields: ['*'], limit: 0 });
    }

    where(filters) {
        this._filters = filters;
        return this;
    }

    async get() {
        return await frappe.db.get_list(this.doctype, {
            filters: this._filters,
            fields: ['*'],
            limit: 0
        });
    }

    async save() {
        if (this.name) {
            // Update
            return await frappe.db.set_value(this.doctype, this.name, this.data);
        } else {
            // Create
            const res = await frappe.db.insert({
                doctype: this.doctype,
                ...this.data
            });
            this.name = res.name;
            return res;
        }
    }


    async delete(name = null) {
        const targetName = name || this.name;
        if (!targetName) {
            frappe.throw(__("Please provide a name or find a record to delete."));
        }

        await frappe.call({
            method: 'frappe.client.delete',
            args: { doctype: this.doctype, name: targetName }
        });

        // Clear the name so goTo() knows the record is gone
        if (targetName === this.name) this.name = null;

        return this;
    }



    // --- SMART NAVIGATION ---
    goTo(name = null) {
        // 1. Prioritize the passed name
        // 2. Fallback to the instance name (set by find() or save())
        const targetName = name || this.name;

        if (targetName) {
            // If we have a name, go to the specific record Form
            frappe.set_route('Form', this.doctype, targetName);
        } else {
            // If no name exists, go to the List View
            frappe.set_route('List', this.doctype);
        }
        return this;
    }


    toast(msg = '') {
        frappe.msgprint(msg)

        return this
    }

}

// Attach to window so it is available globally in the browser
window.ref = (doctype) => new Ref(doctype);
