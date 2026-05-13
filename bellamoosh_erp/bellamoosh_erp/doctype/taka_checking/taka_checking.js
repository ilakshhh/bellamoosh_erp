frappe.ui.form.on('Taka Checking', {

    war_kata_yards(frm) {
        frm.set_value('war_kata_mtrs', (frm.doc.war_kata_yards * 0.9144).toFixed(4));
        calculate_packing(frm);
    },

    wastage(frm) {
        let val = frm.doc.wastage || '';
        if (val.startsWith('=')) {
            try {
                let formula = val.substring(1).replace(/[^0-9.+\-*\s]/g, '');
                let result = Function('"use strict"; return (' + formula + ')')();
                frm.set_value('total_wastage', parseFloat(result.toFixed(4)));
            } catch (e) {
                frappe.msgprint(__('Invalid wastage formula. Use numbers with + - * only.'));
            }
        } else {
            frm.set_value('total_wastage', parseFloat(val) || 0);
        }
        calculate_packing(frm);
    },

    sample(frm) {
        calculate_packing(frm);
    },

    total_wastage(frm) {
        calculate_packing(frm);
    }
});

frappe.ui.form.on('Cutting Detail', {
    cutting_yards(frm) {
        calculate_cutting_sum(frm);
    },
    cutting_details_remove(frm) {
        calculate_cutting_sum(frm);
    }
});

function calculate_packing(frm) {
    let war_kata = frm.doc.war_kata_yards || 0;
    let wastage  = frm.doc.total_wastage || 0;
    let sample   = frm.doc.sample || 0;
    let packing_yds = parseFloat((war_kata - wastage - sample).toFixed(4));
    frm.set_value('packing_qty_yards', packing_yds);
    frm.set_value('packing_qty_mtrs', parseFloat((packing_yds * 0.9144).toFixed(4)));
}

function calculate_cutting_sum(frm) {
    // Recalculate wastage categories after cutting detail changes
    let chindi = 0, fant = 0, good_cut = 0, super_good_cut = 0;
    (frm.doc.cutting_details || []).forEach(row => {
        let y = row.cutting_yards || 0;
        if (y >= 0.1 && y < 0.5)  chindi += y;
        else if (y >= 0.5 && y < 2.0)  fant += y;
        else if (y >= 2.0 && y < 5.0)  good_cut += y;
        else if (y >= 5.0 && y < 7.0)  super_good_cut += y;
    });
    frm.set_value('chindi', parseFloat(chindi.toFixed(4)));
    frm.set_value('fant', parseFloat(fant.toFixed(4)));
    frm.set_value('good_cut', parseFloat(good_cut.toFixed(4)));
    frm.set_value('super_good_cut', parseFloat(super_good_cut.toFixed(4)));
}
