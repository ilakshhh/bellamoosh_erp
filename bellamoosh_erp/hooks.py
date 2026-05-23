app_name = "bellamoosh_erp"
app_title = "Bellamoosh ERP"
app_publisher = "Bellamoosh Lifestyle LLP"
app_description = "Custom Frappe app for Bellamoosh Lifestyle LLP fabric export operations"
app_email = "info@bellamoosh.com"
app_license = "MIT"

# Fixtures — these JSON files are imported when app is installed
fixtures = [
    {"dt": "Role", "filters": [["name", "in", [
        "Surat Operator", "Bhiwandi Operator", "Headoffice Manager", "BLL Management"
    ]]]},
    {"dt": "Custom Field", "filters": [["module", "=", "Bellamoosh ERP"]]},
]

# Document Events
doc_events = {
    "Purchase Receipt": {
        "before_save": "bellamoosh_erp.bellamoosh_erp.doctype.taka_checking.taka_checking.before_save_purchase_receipt",
        "on_submit": "bellamoosh_erp.bellamoosh_erp.doctype.taka_checking.taka_checking.auto_generate_taka_nos",
    },
    "Stock Entry": {
        "on_submit": "bellamoosh_erp.bellamoosh_erp.doctype.taka_checking.taka_checking.update_bale_status",
    },
    "Delivery Note": {
        "on_submit": "bellamoosh_erp.bellamoosh_erp.doctype.carton.carton.mark_cartons_dispatched",
    },
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "bellamoosh_erp.bellamoosh_erp.doctype.taka_checking.taka_checking.flag_overdue_processes",
    ]
}
