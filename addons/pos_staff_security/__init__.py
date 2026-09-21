from . import models


def post_init_hook(env):
    """Create/update the two local-development users after module install."""
    Users = env["res.users"].sudo().with_context(no_reset_password=True)

    # Odoo creates a built-in "Tips" product when Point of Sale is installed.
    # Keep its technical XML ID intact, but archive it so the admin starts with
    # an empty product catalogue and can create every sellable item explicitly.
    tip_product = env.ref(
        "point_of_sale.product_product_tip", raise_if_not_found=False
    )
    if tip_product:
        tip_product.sudo().product_tmpl_id.write({
            "active": False,
            "sale_ok": False,
            "purchase_ok": False,
        })

    admin = Users.search([("login", "=", "admin@gmail.com")], limit=1)
    if not admin:
        # Reuse Odoo's initial administrator so there is still only one admin.
        admin = env.ref("base.user_admin").sudo()
    admin.write({
        "name": "Administrator",
        "login": "admin@gmail.com",
        "email": "admin@gmail.com",
        "password": "password",
        "active": True,
    })

    staff_group = env.ref("pos_staff_security.group_pos_staff_restricted")
    pos_group = env.ref("point_of_sale.group_pos_user")
    internal_group = env.ref("base.group_user")
    staff = Users.search([("login", "=", "staff@gmail.com")], limit=1)
    values = {
        "name": "POS Staff",
        "login": "staff@gmail.com",
        "email": "staff@gmail.com",
        "password": "password",
        "active": True,
        "company_id": admin.company_id.id,
        "company_ids": [(6, 0, admin.company_ids.ids)],
        "groups_id": [(6, 0, (internal_group | pos_group | staff_group).ids)],
    }
    if staff:
        staff.write(values)
    else:
        Users.create(values)
