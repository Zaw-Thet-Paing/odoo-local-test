{
    "name": "Restricted POS Staff",
    "version": "18.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Bootstrap admin and POS-only read-only backend staff",
    "license": "LGPL-3",
    "depends": ["point_of_sale"],
    "data": ["security/security.xml"],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
}
