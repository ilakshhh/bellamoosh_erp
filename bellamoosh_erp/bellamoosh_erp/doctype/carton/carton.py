import frappe
from frappe import _
from frappe.model.document import Document


class Carton(Document):

    def autoname(self):
        self.carton_no = frappe.model.naming.make_autoname("CRTN-.#####.")
        self.name = self.carton_no

    def validate(self):
        self.validate_single_product()
        self.calculate_totals()
        self.calculate_gross_weight()

    def validate_single_product(self):
        products = {row.product for row in self.roll_details if row.product}
        if len(products) > 1:
            frappe.throw(_("All rolls in a Carton must be from the same Product. "
                           "Found: {0}").format(", ".join(products)))

    def calculate_totals(self):
        self.total_rolls = len(self.roll_details)
        self.total_yards = round(sum(row.total_yards or 0 for row in self.roll_details), 4)

    def calculate_gross_weight(self):
        if self.net_weight:
            self.gross_weight = round(self.net_weight + 0.500, 3)

    def on_submit(self):
        for row in self.roll_details:
            frappe.db.set_value("Roll", row.roll_no, "status", "In Carton")
            frappe.db.set_value("Roll", row.roll_no, "carton_no", self.name)


def mark_cartons_dispatched(doc, method):
    """Called via hooks on Delivery Note on_submit"""
    for item in doc.items:
        if item.carton_no:
            frappe.db.set_value("Carton", item.carton_no, "status", "Dispatched")
            frappe.db.set_value("Carton", item.carton_no, "delivery_note_no", doc.name)
