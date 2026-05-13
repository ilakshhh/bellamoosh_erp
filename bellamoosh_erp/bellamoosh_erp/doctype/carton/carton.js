frappe.ui.form.on('Carton', {

    net_weight(frm) {
        frm.set_value('gross_weight', parseFloat((frm.doc.net_weight + 0.500).toFixed(3)));
    },

    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Print Carton Barcode'), () => {
                frappe.utils.print(frm.doctype, frm.docname, 'Carton Barcode');
            });
        }
    }
});

frappe.ui.form.on('Carton Roll Detail', {
    roll_no(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.roll_no) {
            frappe.db.get_value('Roll', row.roll_no, ['color_no', 'total_yards', 'product'], (r) => {
                frappe.model.set_value(cdt, cdn, 'color_no', r.color_no);
                frappe.model.set_value(cdt, cdn, 'total_yards', r.total_yards);
                frappe.model.set_value(cdt, cdn, 'product', r.product);
                update_carton_totals(frm);
            });
        }
    },
    roll_details_remove(frm) { update_carton_totals(frm); }
});

function update_carton_totals(frm) {
    let total = (frm.doc.roll_details || [])
        .reduce((sum, r) => sum + (r.total_yards || 0), 0);
    frm.set_value('total_rolls', (frm.doc.roll_details || []).length);
    frm.set_value('total_yards', parseFloat(total.toFixed(4)));
}
