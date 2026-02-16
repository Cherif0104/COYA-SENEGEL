{
    "name": "COYA Paie",
    "summary": "Bulletins de paie : taux horaire, jours travaillés, défalcations, sanctions, primes Trinité, cotisations (CNSS, AMO, IR, mutuelle)",
    "version": "18.0.1.0.0",
    "author": "SENEGEL",
    "website": "https://coya.pro",
    "category": "COYA",
    "license": "LGPL-3",
    "depends": [
        "hr",
        "hr_contract",
        "coya_presence_policy",
        "coya_trinite",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_company_views.xml",
        "views/hr_contract_views.xml",
        "views/payslip_views.xml",
        "views/menu_views.xml",
    ],
    "installable": True,
    "application": False,
}
