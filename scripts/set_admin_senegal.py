# Script à exécuter dans Odoo shell pour définir le super admin SENEGEL
# Usage: cat set_admin_senegal.py | docker exec -i -e HOST=... -e USER=... -e PASSWORD=... -e PORT=5432 sunugest-odoo-1 odoo shell -d postgres -c /etc/odoo/odoo-supabase.conf --no-http
user = env['res.users'].search([('login', '=', 'admin')], limit=1)
if not user:
    user = env['res.users'].search([('id', '=', 2)], limit=1)
if not user:
    user = env['res.users'].search([('login', '!=', '__system__')], limit=1)
if user:
    user.write({'login': 'techsupport@senegel.org', 'password': 'Alphatango'})
    env.cr.commit()
    print('OK: admin mis a jour -> techsupport@senegel.org / Alphatango')
else:
    print('ERREUR: aucun utilisateur admin trouve')
exit()
