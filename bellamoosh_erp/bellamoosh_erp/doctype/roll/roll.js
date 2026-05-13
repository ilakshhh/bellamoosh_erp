frappe.ui.form.on('Roll', {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Print Roll Barcode'), () => {
                frappe.utils.print(frm.doctype, frm.docname, 'Roll Barcode');
            });
        }
    }
});

frappe.ui.form.on('Roll Cutting Detail', {
    cutting_yards(frm) { update_totals(frm); },
    cutting_details_remove(frm) { update_totals(frm); }
});

function update_totals(frm) {
    let total_yards = (frm.doc.cutting_details || [])
        .reduce((sum, r) => sum + (r.cutting_yards || 0), 0);
    frm.set_value('total_yards', parseFloat(total_yards.toFixed(4)));
    frm.set_value('total_mtrs', parseFloat((total_yards * 0.9144).toFixed(4)));
}
