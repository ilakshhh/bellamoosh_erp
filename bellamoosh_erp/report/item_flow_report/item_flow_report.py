import frappe


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 90},
        {"label": "PO No", "fieldname": "po_no", "fieldtype": "Link", "options": "Purchase Order", "width": 130},
        {"label": "Product", "fieldname": "product", "fieldtype": "Link", "options": "Item", "width": 130},
        {"label": "Color", "fieldname": "color_no", "fieldtype": "Data", "width": 70},
        {"label": "Chart No", "fieldname": "chart_no", "fieldtype": "Data", "width": 90},
        {"label": "PO Qty (Mtrs)", "fieldname": "po_qty", "fieldtype": "Float", "width": 110},
        {"label": "GIN No", "fieldname": "gin_no", "fieldtype": "Data", "width": 110},
        {"label": "GIN Qty (Mtrs)", "fieldname": "gin_qty", "fieldtype": "Float", "width": 110},
        {"label": "Checked Mtrs", "fieldname": "checked_mtrs", "fieldtype": "Float", "width": 110},
        {"label": "Condition", "fieldname": "condition", "fieldtype": "Data", "width": 80},
        {"label": "Bale No", "fieldname": "bale_no", "fieldtype": "Data", "width": 90},
        {"label": "Roll No", "fieldname": "roll_no", "fieldtype": "Data", "width": 90},
        {"label": "Carton No", "fieldname": "carton_no", "fieldtype": "Data", "width": 100},
        {"label": "Delivery Note", "fieldname": "delivery_note", "fieldtype": "Link",
         "options": "Delivery Note", "width": 130},
    ]


def get_data(filters):
    conditions = ""
    if filters.get("chart_no"):
        conditions += " AND pri.chart_no = %(chart_no)s"
    if filters.get("supplier"):
        conditions += " AND pr.supplier = %(supplier)s"
    if filters.get("from_date"):
        conditions += " AND pr.posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND pr.posting_date <= %(to_date)s"

    return frappe.db.sql(f"""
        SELECT
            pr.posting_date       AS date,
            poi.parent            AS po_no,
            pri.item_code         AS product,
            pri.color_no,
            pri.chart_no,
            poi.qty               AS po_qty,
            pr.name               AS gin_no,
            pri.qty               AS gin_qty,
            pri.checked_mtrs,
            pri.condition,
            se.bale_no,
            r.name                AS roll_no,
            c.name                AS carton_no,
            c.delivery_note_no    AS delivery_note
        FROM
            `tabPurchase Receipt` pr
            JOIN `tabPurchase Receipt Item` pri ON pri.parent = pr.name
            LEFT JOIN `tabPurchase Order Item` poi
                ON poi.parent = pri.purchase_order AND poi.item_code = pri.item_code
            LEFT JOIN `tabStock Entry` se ON se.purpose = 'Material Transfer'
            LEFT JOIN `tabRoll` r ON r.chart_no = pri.chart_no AND r.color_no = pri.color_no
            LEFT JOIN `tabCarton` c ON c.chart_no = pri.chart_no
        WHERE
            pr.docstatus = 1
            {conditions}
        ORDER BY pr.posting_date DESC
        LIMIT 500
    """, filters, as_dict=True)
