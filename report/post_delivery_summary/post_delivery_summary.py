import frappe


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 90},
        {"label": "Chart No", "fieldname": "chart_no", "fieldtype": "Data", "width": 100},
        {"label": "Supplier", "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 130},
        {"label": "Color", "fieldname": "color_no", "fieldtype": "Data", "width": 70},
        {"label": "Order Qty", "fieldname": "order_qty", "fieldtype": "Float", "width": 90},
        {"label": "Checked Qty", "fieldname": "checked_qty", "fieldtype": "Float", "width": 100},
        {"label": "Received Qty", "fieldname": "received_qty", "fieldtype": "Float", "width": 100},
        {"label": "Return Qty", "fieldname": "return_qty", "fieldtype": "Float", "width": 90},
        {"label": "Total Pack Qty", "fieldname": "total_pack_qty", "fieldtype": "Float", "width": 110},
        {"label": "Total Pcs", "fieldname": "total_pcs", "fieldtype": "Int", "width": 80},
        {"label": "Wastage", "fieldname": "wastage", "fieldtype": "Float", "width": 80},
        {"label": "Loss %", "fieldname": "loss_pct", "fieldtype": "Percent", "width": 80},
        {"label": "Delivery Date", "fieldname": "delivery_date", "fieldtype": "Date", "width": 100},
        {"label": "Delivery Note", "fieldname": "delivery_note", "fieldtype": "Link",
         "options": "Delivery Note", "width": 130},
        {"label": "Invoice Date", "fieldname": "invoice_date", "fieldtype": "Date", "width": 100},
    ]


def get_data(filters):
    conditions = ""
    if filters.get("chart_no"):
        conditions += " AND dni.chart_no = %(chart_no)s"
    if filters.get("from_date"):
        conditions += " AND dn.posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND dn.posting_date <= %(to_date)s"

    rows = frappe.db.sql(f"""
        SELECT
            dn.posting_date         AS date,
            dni.chart_no,
            dn.supplier_name        AS supplier,
            dni.color_no,
            so_item.qty             AS order_qty,
            pri.checked_mtrs        AS checked_qty,
            pri.qty                 AS received_qty,
            0                       AS return_qty,
            dni.qty                 AS total_pack_qty,
            c.total_rolls           AS total_pcs,
            tc.total_wastage        AS wastage,
            dn.posting_date         AS delivery_date,
            dn.name                 AS delivery_note,
            si.posting_date         AS invoice_date
        FROM
            `tabDelivery Note` dn
            JOIN `tabDelivery Note Item` dni ON dni.parent = dn.name
            LEFT JOIN `tabSales Order Item` so_item
                ON so_item.parent = dn.sales_order AND so_item.chart_no = dni.chart_no
            LEFT JOIN `tabPurchase Receipt Item` pri ON pri.chart_no = dni.chart_no AND pri.color_no = dni.color_no
            LEFT JOIN `tabCarton` c ON c.delivery_note_no = dn.name AND c.chart_no = dni.chart_no
            LEFT JOIN `tabTaka Checking` tc ON tc.chart_no = dni.chart_no AND tc.color_no = dni.color_no
            LEFT JOIN `tabSales Invoice Item` sii ON sii.delivery_note = dn.name
            LEFT JOIN `tabSales Invoice` si ON si.name = sii.parent AND si.docstatus = 1
        WHERE
            dn.docstatus = 1
            {conditions}
        ORDER BY dn.posting_date DESC
    """, filters, as_dict=True)

    for row in rows:
        if row.checked_qty and row.wastage:
            row.loss_pct = round((row.wastage / row.checked_qty) * 100, 2)
        else:
            row.loss_pct = 0.0

    return rows
