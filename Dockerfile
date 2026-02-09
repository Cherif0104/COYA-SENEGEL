# COYA.PRO – Image Odoo 18 + addons SENEGEL pour Render (et autres PaaS Docker)
# Base officielle Odoo ; connexion DB via variables d'environnement (Supabase).
#
# Sur Render, définir dans Environment Variables :
#   DB_HOST, DB_USER, DB_PASSWORD, DB_PORT=5432  (Supabase pooler)
#   PORT est fourni par Render (port HTTP, ex. 10000)

FROM odoo:18

USER root
COPY addons/custom /mnt/extra-addons
COPY config/odoo-supabase.conf /etc/odoo/odoo-supabase.conf
RUN chown -R odoo:odoo /mnt/extra-addons
USER odoo

EXPOSE 8069

# Connexion Supabase via DB_* ; port HTTP = PORT (Render)
CMD ["sh", "-c", "exec odoo -c /etc/odoo/odoo-supabase.conf --db_host=\"$DB_HOST\" --db_user=\"$DB_USER\" --db_password=\"$DB_PASSWORD\" --db_port=\"${DB_PORT:-5432}\" --http-port=${PORT:-8069}"]
