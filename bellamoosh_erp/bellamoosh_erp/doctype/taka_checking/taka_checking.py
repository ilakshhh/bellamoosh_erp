import frappe
from frappe import _
from frappe.model.document import Document


class TakaChecking(Document):

    def validate(self):
        self.calculate_war_kata_metres()
        self.parse_wastage_formula()
        self.calculate_packing_qty()
        self.validate_packing_qty()
        self.categorise_wastage()
        self._auto_link_purchase_receipt()

    def on_submit(self):
        self._update_pr_taka_row()

    def calculate_war_kata_metres(self):
        if self.war_kata_yards:
            self.war_kata_mtrs = round(self.war_kata_yards * 0.9144, 4)

    def parse_wastage_formula(self):
        """Allow user to enter wastage as formula like =0.4+1.99+5+2.99"""
        if self.wastage and str(self.wastage).startswith("="):
            try:
                formula = self.wastage[1:]
                # Only allow safe numeric operations
                allowed = set("0123456789.+-* ")
                if all(c in allowed for c in formula):
                    self.total_wastage = round(eval(formula), 4)  # noqa
                else:
                    frappe.throw(_("Wastage formula contains invalid characters. Use numbers and + - * only."))
            except Exception:
                frappe.throw(_("Could not evaluate wastage formula: {0}").format(self.wastage))
        elif self.wastage:
            try:
                self.total_wastage = float(self.wastage)
            except ValueError:
                frappe.throw(_("Wastage must be a number or formula starting with ="))

    def calculate_packing_qty(self):
        war_kata = self.war_kata_yards or 0
        wastage = self.total_wastage or 0
        sample = self.sample or 0
        self.packing_qty_yards = round(war_kata - wastage - sample, 4)
        self.packing_qty_mtrs = round(self.packing_qty_yards * 0.9144, 4)

    def validate_packing_qty(self):
        expected = round((self.war_kata_yards or 0) - (self.total_wastage or 0) - (self.sample or 0), 4)
        if abs((self.packing_qty_yards or 0) - expected) > 0.01:
            frappe.throw(
                _("Packing Qty (Yard) does not match with (War Kata(Yard) - Sample - Wastage). "
                  "Expected: {0}, Got: {1}").format(expected, self.packing_qty_yards)
            )

    def categorise_wastage(self):
        """Parse cutting details and auto-assign to Chindi/Fant/Good Cut/Super Good Cut"""
        chindi = fant = good_cut = super_good_cut = 0.0
        for row in self.cutting_details:
            yds = row.cutting_yards or 0
            if 0.1 <= yds < 0.5:
                chindi += yds
            elif 0.5 <= yds < 2.0:
                fant += yds
            elif 2.0 <= yds < 5.0:
                good_cut += yds
            elif 5.0 <= yds < 7.0:
                super_good_cut += yds
        self.chindi = round(chindi, 4)
        self.fant = round(fant, 4)
        self.good_cut = round(good_cut, 4)
        self.super_good_cut = round(super_good_cut, 4)

    def _auto_link_purchase_receipt(self):
        """Look up which Purchase Receipt this taka came from and link it."""
        if self.taka_no and not self.purchase_receipt:
            pr_name = frappe.db.get_value(
                "Purchase Receipt Taka Detail",
                {"taka_no": self.taka_no},
                "parent",
            )
            if pr_name:
                self.purchase_receipt = pr_name

    def _update_pr_taka_row(self):
        """On submit, write QC results back to the Purchase Receipt taka row."""
        if not self.taka_no:
            return
        row_name = frappe.db.get_value(
            "Purchase Receipt Taka Detail",
            {"taka_no": self.taka_no},
            "name",
        )
        if row_name:
            frappe.db.set_value("Purchase Receipt Taka Detail", row_name, {
                "taka_checking": self.name,
                "wastage": self.total_wastage,
                "packing_qty_yards": self.packing_qty_yards,
                "packing_qty_mtrs": self.packing_qty_mtrs,
                "status": self.status,
                "checked_date": self.received_date,
            })


# ── Purchase Receipt hooks ────────────────────────────────────────────────────

def before_save_purchase_receipt(doc, method):
    """Single entry point for all PR before_save logic."""
    _calculate_taka_detail_mtrs(doc)
    _validate_challan_duplicate(doc)


def _calculate_taka_detail_mtrs(doc):
    """Auto-calculate war_kata_mtrs for each taka_details row."""
    for row in getattr(doc, "taka_details", []):
        if row.war_kata_yards:
            row.war_kata_mtrs = round(row.war_kata_yards * 0.9144, 4)


def _validate_challan_duplicate(doc):
    challan_no = getattr(doc, "challan_no", None)
    if challan_no and doc.supplier:
        existing = frappe.db.exists("Purchase Receipt", {
            "challan_no": challan_no,
            "supplier": doc.supplier,
            "name": ("!=", doc.name),
            "docstatus": ("!=", 2),
        })
        if existing:
            frappe.throw(
                _("Challan No {0} already exists for supplier {1} in {2}. "
                  "Same challan is allowed for different suppliers only.").format(
                    challan_no, doc.supplier, existing)
            )


def auto_generate_taka_nos(doc, method):
    """
    On PR submit, stamp a Taka No on every taka_details row.
    Falls back to items rows if taka_details is empty (backward compat).
    Format: ChartNo-SupplierCode-ColorNo-GINNo-T{seq}
    """
    supplier_code = (
        frappe.db.get_value("Supplier", doc.supplier, "abbr") or doc.supplier[:2].upper()
    )
    gin_no = doc.name.replace("/", "-")
    taka_details = getattr(doc, "taka_details", [])

    if taka_details:
        for idx, row in enumerate(taka_details, start=1):
            if not row.taka_no:
                chart = getattr(doc, "chart_no", None) or "XX"
                color = row.color_no or "00"
                row.taka_no = f"{chart}-{supplier_code}-{color}-{gin_no}-T{idx}"
    else:
        # Legacy: generate one taka per item row
        for idx, row in enumerate(doc.items, start=1):
            if not getattr(row, "taka_no", None):
                chart = getattr(row, "chart_no", None) or "XX"
                color = getattr(row, "color_no", None) or "00"
                row.taka_no = f"{chart}-{supplier_code}-{color}-{gin_no}-T{idx}"

    doc.save()


# ── Stock Entry hook ──────────────────────────────────────────────────────────

def update_bale_status(doc, method):
    """When a Stock Entry (bale transfer) is submitted, update taka status"""
    if doc.purpose == "Material Transfer":
        for row in doc.items:
            if row.serial_no:
                frappe.db.set_value("Serial No", row.serial_no, "warehouse", doc.to_warehouse)


# ── Scheduled task ────────────────────────────────────────────────────────────

def flag_overdue_processes(doc=None, method=None):
    """Daily: flag any sub-contractor processes overdue"""
    overdue = frappe.get_all(
        "Subcontracting Order",
        filters={"status": "Open", "delivery_date": ("<", frappe.utils.today())},
        fields=["name", "supplier", "delivery_date"],
    )
    for item in overdue:
        frappe.logger().warning(f"Overdue sub-contractor process: {item.name} due {item.delivery_date}")
