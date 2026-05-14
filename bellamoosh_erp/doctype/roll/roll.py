import frappe
from frappe import _
from frappe.model.document import Document


class Roll(Document):

    def autoname(self):
        self.roll_no = frappe.model.naming.make_autoname("ROLL-.#####.")
        self.name = self.roll_no

    def validate(self):
        self.validate_single_product()
        self.validate_single_color()
        self.calculate_totals()

    def validate_single_product(self):
        products = {row.product for row in self.cutting_details if row.product}
        if len(products) > 1:
            frappe.throw(_("All cutting pieces in a Roll must be from the same Product. "
                           "Found: {0}").format(", ".join(products)))

    def validate_single_color(self):
        colors = {row.color_no for row in self.cutting_details if row.color_no}
        if len(colors) > 1:
            frappe.throw(_("All cutting pieces in a Roll must have the same Color No. "
                           "Found: {0}").format(", ".join(colors)))

    def calculate_totals(self):
        self.total_yards = round(sum(row.cutting_yards or 0 for row in self.cutting_details), 4)
        self.total_mtrs = round(self.total_yards * 0.9144, 4)
