def post_init_hook(env):
    """Create/update the sole local-development administrator."""
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
        "group_ids": [(4, env.ref("base.group_system").id)],
    })

    # Remove access for the staff account created by earlier module versions.
    # Archiving is safer than deletion because business records may reference it.
    staff = Users.with_context(active_test=False).search([
        ("login", "=", "staff@gmail.com"),
    ])
    if staff:
        staff.write({"active": False})
