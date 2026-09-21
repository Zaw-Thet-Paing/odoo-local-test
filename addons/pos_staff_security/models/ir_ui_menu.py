from odoo import api, models


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    @api.model
    def _visible_menu_ids(self, debug=False):
        visible = super()._visible_menu_ids(debug=debug)
        if self.env.su or not self.env.user.has_group(
            "pos_staff_security.group_pos_staff_restricted"
        ):
            return visible

        pos_root = self.env.ref("point_of_sale.menu_point_root", False)
        if not pos_root:
            return visible
        # ``ir.ui.menu.search`` applies visibility filtering and would call
        # this method again.  Sudo is safe here: we only use it to determine
        # the POS tree, then intersect it with the already access-checked set.
        allowed = self.sudo().search([("id", "child_of", pos_root.id)]).ids
        return visible & set(allowed)
