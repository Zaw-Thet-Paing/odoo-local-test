from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _as_pos_transaction(self):
        return self.with_context(pos_staff_pos_transaction=True)

    def set_opening_control(self, cashbox_value, notes):
        session = self._as_pos_transaction()
        return super(PosSession, session).set_opening_control(cashbox_value, notes)

    def delete_opening_control_session(self):
        session = self._as_pos_transaction()
        return super(PosSession, session).delete_opening_control_session()

    def update_closing_control_state_session(self, notes):
        session = self._as_pos_transaction()
        return super(PosSession, session).update_closing_control_state_session(notes)

    def post_closing_cash_details(self, counted_cash):
        session = self._as_pos_transaction()
        return super(PosSession, session).post_closing_cash_details(counted_cash)

    def action_pos_session_closing_control(
        self,
        balancing_account=False,
        amount_to_balance=0,
        bank_payment_method_diffs=None,
    ):
        session = self._as_pos_transaction()
        return super(PosSession, session).action_pos_session_closing_control(
            balancing_account=balancing_account,
            amount_to_balance=amount_to_balance,
            bank_payment_method_diffs=bank_payment_method_diffs,
        )
