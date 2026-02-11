# Même script que set_admin_senegal.py (alias pour éviter la faute de frappe)
user = env['res.users'].search([('login', '=', 'admin')], limit=1)
if not user:
    user = env['res.users'].search([('id', '=', 2)], limit=1)
if not user:
    user = env['res.users'].search([('login', '!=', '__system__')], limit=1)
if user:
    user.write({'login': 'techsupport@senegel.com', 'password': 'Alphatango2026@'})
    env.cr.commit()
    print('OK: admin mis a jour -> techsupport@senegel.com / Alphatango2026@')
else:
    print('ERREUR: aucun utilisateur admin trouve')
exit()
