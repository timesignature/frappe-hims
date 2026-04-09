// Copyright (c) 2026, Shelton Tembo and contributors
// For license information, please see license.txt




frappe.ui.form.on("Episode", {
    refresh(frm) {

        frm.dashboard.links_area.body.find('.btn-new[data-doctype="Sales Invoice"]').hide();


        frm.add_custom_button('Bill Invoice', () => {

            frappe.route_options = {
                customer: frm.doc.patient_no,
                episode_no: frm.doc.name,
                is_hospital_bill: 1
            }

            frappe.set_route('Form', 'Sales Invoice', 'new-sales-invoice')

        })


        frm.add_custom_button('Discharge Patient', () => {
            if (frm.doc.status === 'Open') {
                let d = new frappe.ui.Dialog({
                    title: 'Discharge',
                    fields: [
                        {
                            label: 'Episode No.',
                            fieldname: 'episode_no',
                            fieldtype: 'Data',
                            default: frm.doc.name
                        },


                        {
                            label: 'Discharge Date',
                            fieldname: 'discharge_date',
                            fieldtype: 'Datetime',
                            default: frappe.datetime.now_datetime()
                        },


                        {
                            label: 'Discharge Status',
                            fieldname: 'discharge_status',
                            fieldtype: 'Select',
                            options: ['Stable', 'Death', 'Referred'],
                            reqd: 1
                        },

                        {
                            label: 'Discharge Notes',
                            fieldname: 'discharge_note',
                            fieldtype: 'Small Text',
                            reqd: 1
                        }
                    ],
                    size: 'small', // small, large, extra-large 
                    primary_action_label: 'Admit Patient',
                    async primary_action(values) {

                        const doc = await ref('Episode').find(frm.doc.name)
                        doc.status = 'Closed'
                        doc.discharge_date = values.discharge_date
                        doc.discharge_comment = values.discharge_note
                        doc.discharge_status = values.discharge_status
                        await doc.save()
                        d.hide()

                        frm.refresh()
                    }
                });

                d.show();
            } else {
                frappe.throw(`Episode has been [${frm.doc.status}]`)
                return
            }
        })

        frm.add_custom_button('Vitals', () => {
            frappe.route_options = {
                "episode_no": frm.doc.name,
                'date_created': frappe.datetime.now_datetime()
            };

            // 2. Route to the new form
            frappe.set_route('Form', 'Vital', 'new-vital');
        }, 'Clinical Activities')
        frm.add_custom_button('Clinical Notes', () => {

            frappe.route_options = {
                "episode_no": frm.doc.name,
                'date_created': frappe.datetime.now_datetime()
            };

            // 2. Route to the new form
            frappe.set_route('Form', 'Clinical Note', 'new-clinical-note');
        }, 'Clinical Activities')
        frm.add_custom_button('Diagnosis', () => { }, 'Clinical Activities')
        frm.add_custom_button('Prescription', () => {
            frappe.route_options = {
                "episode_no": frm.doc.name,
                'date_created': frappe.datetime.now_datetime()
            };

            // 2. Route to the new form
            frappe.set_route('Form', 'Prescription', 'new-prescription');
        }, 'Clinical Activities')



        frm.add_custom_button('Generate Claim', async () => {

            const doc = await ref('Sales Invoice').where({
                episode_no: frm.doc.name
            }).get()

            console.log(doc)



        }, 'Clinical Activities')






    },
});
