import frappe


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Chart No", "fieldname": "chart_no", "fieldtype": "Data", "width": 100},
        {"label": "Supplier", "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 130},
        {"label": "Color No", "fieldname": "color_no", "fieldtype": "Data", "width": 80},
        {"label": "PO Qty", "fieldname": "po_qty", "fieldtype": "Float", "width": 90},
        {"label": "Checked Qty", "fieldname": "checked_qty", "fieldtype": "Float", "width": 100},
        {"label": "Return Qty", "fieldname": "return_qty", "fieldtype": "Float", "width": 90},
        {"label": "War Kata (Yds)", "fieldname": "war_kata_yards", "fieldtype": "Float", "width": 110},
        {"label": "Chindi", "fieldname": "chindi", "fieldtype": "Float", "width": 80},
        {"label": "Fant", "fieldname": "fant", "fieldtype": "Float", "width": 80},
        {"label": "Good Cut", "fieldname": "good_cut", "fieldtype": "Float", "width": 90},
        {"label": "Super Good Cut", "fieldname": "super_good_cut", "fieldtype": "Float", "width": 110},
        {"label": "Total Wastage", "fieldname": "total_wastage", "fieldtype": "Float", "width": 100},
        {"label": "Packing Qty (Yds)", "fieldname": "packing_qty_yards", "fieldtype": "Float", "width": 120},
        {"label": "Roll No", "fieldname": "roll_no", "fieldtype": "Data", "width": 100},
        {"label": "Carton No", "fieldname": "carton_no", "fieldtype": "Data", "width": 100},
        {"label": "Delivery Note", "fieldname": "delivery_note", "fieldtype": "Link",
         "options": "Delivery Note", "width": 130},
    ]


def get_data(filters):
    conditions = ""
    if filters.get("chart_no"):
        conditions += " AND tc.chart_no = %(chart_no)s"
    if filters.get("color_no"):
        conditions += " AND tc.color_no = %(color_no)s"

    return frappe.db.sql(f"""
        SELECT
            tc.chart_no,
            tc.supplier,
            tc.color_no,
            pri.qty          AS po_qty,
            tc.war_kata_yards,
            tc.chindi,
            tc.fant,
            tc.good_cut,
            tc.super_good_cut,
            tc.total_wastage,
            tc.packing_qty_yards,
            pri.checked_mtrs AS checked_qty,
            0                AS return_qty,
            r.name           AS roll_no,
            c.name           AS carton_no,
            c.delivery_note_no AS delivery_note
        FROM
            `tabTaka Checking` tc
            LEFT JOIN `tabPurchase Receipt Item` pri ON pri.taka_no = tc.taka_no
            LEFT JOIN `tabRoll Cutting Detail` rcd ON rcd.taka_no = tc.taka_no
            LEFT JOIN `tabRoll` r ON r.name = rcd.parent
            LEFT JOIN `tabCarton Roll Detail` crd ON crd.roll_no = r.name
            LEFT JOIN `tabCarton` c ON c.name = crd.parent
        WHERE
            tc.docstatus = 1
            {conditions}
        ORDER BY tc.chart_no, tc.color_no
    """, filters, as_dict=True)
