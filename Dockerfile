FROM odoo:19.0

USER root

# Keep deploy-time configuration and custom modules inside the image. This
# avoids host bind mounts, whose relative paths Coolify stores separately.
COPY --chown=odoo:odoo config/odoo.conf /etc/odoo/odoo.conf
COPY --chown=odoo:odoo addons/ /mnt/extra-addons/

USER odoo
