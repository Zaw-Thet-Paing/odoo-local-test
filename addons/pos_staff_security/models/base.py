from odoo import _, api, models
from odoo.exceptions import AccessError


class Base(models.AbstractModel):
    _inherit = "base"

    # Live browser infrastructure must update presence outside a sale call.
    # Business writes are instead enabled only by the scoped POS entry points
    # in pos_order.py and pos_session.py.
    _pos_staff_writable_models = {
        "bus.bus",
        "bus.presence",
    }

    def _pos_staff_check_write(self):
        if (
            not self.env.su
            and not self.env.context.get("pos_staff_pos_transaction")
            and self.env.user.has_group(
                "pos_staff_security.group_pos_staff_restricted"
            )
            and self._name not in self._pos_staff_writable_models
        ):
            raise AccessError(
                _("This POS staff account has read-only backend access.")
            )

    @api.model_create_multi
    def create(self, vals_list):
        self._pos_staff_check_write()
        return super().create(vals_list)

    def write(self, vals):
        self._pos_staff_check_write()
        return super().write(vals)

    def unlink(self):
        self._pos_staff_check_write()
        return super().unlink()
