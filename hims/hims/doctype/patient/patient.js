// Copyright (c) 2026, Shelton Tembo and contributors
// For license information, please see license.txt

frappe.ui.form.on("Patient", {
    refresh(frm) {


        frm.dashboard.links_area.body.find('.btn-new').hide();


        frm.set_query('clergy', () => {
            return {
                filters: {
                    'religion': frm.doc.religion
                }
            }
        })




        frm.add_custom_button('Register Visit', async () => {

            const doc = await ref('Episode').where({
                'status': 'Open'
            }).get()

            if (doc.length > 0) {
                frappe.throw(`Patient ${frm.doc.first_name} ${frm.doc.last_name} has an open episode`)
                return
            }


            let d = new frappe.ui.Dialog({
                title: 'Patient Pre-Admission',
                fields: [
                    {
                        label: 'First Name',
                        fieldname: 'first_name',
                        fieldtype: 'Data',
                        default: frm.doc.first_name
                    },
                    {
                        label: 'Last Name',
                        fieldname: 'last_name',
                        fieldtype: 'Data',
                        default: frm.doc.last_name
                    },

                    {
                        label: 'Admission Type',
                        fieldname: 'admission_type',
                        fieldtype: 'Select',
                        options: ['OPD', 'IPD']
                    }
                ],
                size: 'small', // small, large, extra-large 
                primary_action_label: 'Admit Patient',
                async primary_action(values) {

                    const doc = ref('Episode')
                    doc.patient_no = frm.doc.name
                    doc.admission_type = values.admission_type
                    doc.admission_date = frappe.datetime.now_datetime()
                    await doc.save()
                    d.hide();


                    frappe.set_route('Form', 'Episode', doc.name)
                }
            });

            d.show();




        }, 'Activities')


        frm.add_custom_button('Pharmacy Invoice', () => {


            // console.log(frm.doc)

        }, 'Activities')



    },


});
