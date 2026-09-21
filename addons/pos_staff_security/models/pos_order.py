from odoo import api, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def sync_from_ui(self, orders):
        """Allow writes produced internally by a genuine POS sale.

        Validation can create an invoice, journal items and stock moves in
        addition to the POS order itself.  The context flag is scoped to this
        POS synchronization call, so those models remain read-only when the
        cashier visits their backend views directly.
        """
        pos_order = self.with_context(pos_staff_pos_transaction=True)
        return super(PosOrder, pos_order).sync_from_ui(orders)
